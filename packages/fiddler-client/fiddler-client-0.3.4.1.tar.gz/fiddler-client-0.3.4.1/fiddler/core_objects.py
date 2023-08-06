# TODO: Add License

import enum
import functools
import json
import textwrap
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Union
)

import pandas as pd
import pandas.api.types


@enum.unique
class DataType(enum.Enum):
    """Supported datatypes for the Fiddler engine."""
    FLOAT = 'float'
    INTEGER = 'int'
    BOOLEAN = 'bool'
    STRING = 'str'
    CATEGORY = 'category'


@enum.unique
class ModelTask(enum.Enum):
    """Supported model tasks for the Fiddler engine."""
    BINARY_CLASSIFICATION = 'binary_classification'
    MULTICLASS_CLASSIFICATION = 'multiclass_classification'
    REGRESSION = 'regression'


@enum.unique
class ModelInputType(enum.Enum):
    """Supported model paradigms for the Fiddler engine."""
    TABULAR = 'structured'
    TEXT = 'text'


class AttributionExplanation(NamedTuple):
    """The results of an attribution explanation run by the Fiddler engine."""
    algorithm: str
    inputs: List[str]
    attributions: List[float]
    misc: Optional[dict]

    @classmethod
    def from_dict(cls, deserialized_json: dict):
        """Converts a deserialized JSON format into an
        AttributionExplanation object"""
        algorithm = deserialized_json.pop('explanation_type')
        inputs, attributions = zip(
            *deserialized_json.pop('explanation').items())
        return cls(
            algorithm=algorithm,
            inputs=list(inputs),
            attributions=list(attributions),
            misc=deserialized_json
        )


class MulticlassAttributionExplanation(NamedTuple):
    """A collection of AttributionExplanation objects explaining several
    classes' predictions in a multiclass classification setting."""
    classes: Tuple[str]
    explanations: Dict[str, AttributionExplanation]

    @classmethod
    def from_dict(cls, deserialized_json: dict):
        """Converts a deserialized JSON format into an
        MulticlassAttributionExplanation object"""
        return cls(
            classes=tuple(deserialized_json.keys()),
            explanations={
                label_class:
                    AttributionExplanation.from_dict(explanation_dict)
                for label_class, explanation_dict in deserialized_json.items()
            }
        )


class Column:
    """Represents a single column of a dataset or model input/output.

    :param name: The name of the column (corresponds to the header row of a
        CSV file)
    :param data_type: The best encoding type for this column's data.
    :param possible_values: If data_type is CATEGORY, then an exhaustive list
        of possible values for this category must be provided. Otherwise
        this field has no effect and is optional.
    """

    def __init__(self, name: str, data_type: DataType,
                 possible_values: Optional[List[Any]] = None):
        self.name = name
        self.data_type = data_type
        self.possible_values = possible_values

    @classmethod
    def from_dict(cls, desrialized_json: dict):
        """Creates a Column object from deserialized JSON"""
        return cls(
            name=desrialized_json['column-name'],
            data_type=DataType(desrialized_json['data-type']),
            possible_values=desrialized_json.get('possible-values', None)
        )

    def __repr__(self):
        return (f'Column(name="{self.name}", data_type={self.data_type}, '
                f'possible_values={self.possible_values})')

    def _raise_on_bad_categorical(self):
        """Raises a ValueError if data_type=CATEGORY without possible_values"""
        if (self.data_type.value == DataType.CATEGORY.value
                and self.possible_values is None):
            raise ValueError(
                f'Mal-formed categorical column missing `possible_values`: '
                f'{self}')

    def get_pandas_dtype(self):
        """Converts the data_type field to a Pandas-friendly form."""
        self._raise_on_bad_categorical()
        if self.data_type.value == DataType.CATEGORY.value:
            return pandas.api.types.CategoricalDtype(self.possible_values)
        else:
            return self.data_type.value

    def to_dict(self) -> Dict[str, Any]:
        """Converts this object to a more JSON-friendly form."""
        res = {
            'column-name': self.name,
            'data-type': self.data_type.value,
        }
        if self.possible_values is not None:
            # NOTE: we enforce that possible values must be strings
            res['possible-values'] = [str(val) for val in self.possible_values]
        return res


class DatasetInfo:
    """Information about a dataset. Defines the schema.

    :param display_name: A name for user-facing display (different from an id).
    :param columns: A list of Column objects.
    :param files: Optional. If the dataset is stored in one or more CSV files
        with canonical names, this field lists those files. Primarily for use
        only internally to the Fiddler engine.
    """

    def __init__(self, display_name: str, columns: List[Column],
                 files: Optional[List[str]] = None):
        self.display_name = display_name
        self.columns = columns
        self.files = files if files is not None else list()

    def to_dict(self) -> Dict[str, Any]:
        """Converts this object to a more JSON-friendly form."""
        return {
            'name': self.display_name,
            'columns': [c.to_dict() for c in self.columns],
            'files': self.files
        }

    def get_column_names(self) -> List[str]:
        """Returns a list of column names."""
        return [column.name for column in self.columns]

    def get_column_pandas_dtypes(self) -> \
            Dict[str, Union[str, pandas.api.types.CategoricalDtype]]:
        """Get a dictionary describing the pandas datatype of every column."""
        dtypes = dict()
        for column in self.columns:
            dtypes[column.name] = column.get_pandas_dtype()
        return dtypes

    @staticmethod
    def _datatype_from_pandas_dtype(pandas_col) -> DataType:
        dtype_obj = pandas_col.dtype
        # catch uint8 one-hot encoded variables
        if dtype_obj.name == 'uint8' and pandas_col.nunique() < 3:
            return DataType.BOOLEAN

        if dtype_obj.kind == 'i':
            return DataType.INTEGER
        elif dtype_obj.kind == 'f':
            return DataType.FLOAT
        elif dtype_obj.kind == 'b':
            return DataType.BOOLEAN
        elif dtype_obj.kind and dtype_obj.name == 'category':
            return DataType.CATEGORY
        else:
            return DataType.STRING

    @classmethod
    def from_dataframe(cls,
                       df: Union[pd.DataFrame, Iterable[pd.DataFrame]],
                       display_name: str = '',
                       max_inferred_cardinality: Optional[int] = None):
        """Infers a DatasetInfo object from a pandas DataFrame
        (or iterable of DataFrames).

        :param df: Either a single DataFrame or an iterable of DataFrame
            objects. If an iterable is given, all dataframes must have the
            same columns.
        :param display_name: A name for user-facing display (different from
            an id).
        :param max_inferred_cardinality: Optional. If not None, any
            string-typed column with fewer than `max_inferred_cardinality`
            unique values will be inferred as a category (useful for cases
            where use of the built-in CategoricalDtype functionality of Pandas
            is not desired).

        :returns: A DatasetInfo object.
        """
        # if an iterable is passed, infer for each in the iterable and combine
        if not isinstance(df, pd.DataFrame):
            info_gen = (
                cls.from_dataframe(
                    item, max_inferred_cardinality=max_inferred_cardinality)
                for item in df
            )
            return cls.as_combination(info_gen, display_name=display_name)

        columns = []
        if df.index.name is not None:
            id_name = df.index.name
            id_data_type = cls._datatype_from_pandas_dtype(df.index)
            id_column_info = Column(name=id_name, data_type=id_data_type)
            columns.append(id_column_info)
        for column_name, column_series in df.iteritems():
            column_dtype = cls._datatype_from_pandas_dtype(column_series)

            # infer categorical if configured to do so
            if (max_inferred_cardinality is not None
                    and column_dtype.value == DataType.STRING.value
                    and (column_series.nunique() < max_inferred_cardinality)):
                column_dtype = DataType.CATEGORY

            # get possible values for categorical type
            if column_dtype.value == DataType.CATEGORY.value:
                possible_values = column_series.unique().tolist()
            else:
                possible_values = None

            column_info = Column(
                name=column_name,
                data_type=column_dtype,
                possible_values=possible_values
            )
            columns.append(column_info)
        return cls(display_name, columns)

    @classmethod
    def from_dict(cls, deserialized_json: dict):
        """Transforms deserialized JSON into a DatasetInfo object"""
        # drop down into the "dataset" object inside the deserialized_json
        deserialized_json = deserialized_json['dataset']

        # instantiate the class
        return cls(
            display_name=deserialized_json['name'],
            columns=[Column.from_dict(c)
                     for c in deserialized_json['columns']],
            files=deserialized_json.get('files', None),
        )

    @classmethod
    def _combine(cls, info_a, info_b,
                 display_name: str = ''):
        # raise error if column names are incompatible
        if info_a.get_column_names() != info_b.get_column_names():
            raise ValueError(
                f'Incompatible DatasetInfo objects: column names do not '
                f'match:\n{info_a.get_column_names()}\n'
                f'{info_b.get_column_names()}')

        # combine columns
        columns = list()
        for a_column, b_column in zip(info_a.columns, info_b.columns):
            if a_column.data_type.value != b_column.data_type.value:
                raise ValueError(
                    f'Incompatible DatasetInfo objects: column '
                    f'"{a_column.name}" has a data_type mismatch: '
                    f'{a_column.data_type} vs. {b_column.data_type}')
            if a_column.data_type.value == DataType.CATEGORY.value:
                assert a_column.possible_values is not None
                assert b_column.possible_values is not None
                possible_values = list(set(a_column.possible_values)
                                       | set(b_column.possible_values))
            else:
                possible_values = None
            columns.append(Column(a_column.name, a_column.data_type,
                                  possible_values))

        # combine file lists
        files = info_a.files + info_b.files

        return cls(display_name, columns, files)

    @classmethod
    def as_combination(cls, infos: Iterable,
                       display_name: str = 'combined_dataset'):
        """Combines an iterable of compatible DatasetInfo objects into one
        DatasetInfo"""
        return functools.reduce(
            lambda a, b: cls._combine(a, b, display_name=display_name), infos)

    @staticmethod
    def get_summary_dataframe(dataset_info):
        """Returns a table (pandas DataFrame) summarizing the DatasetInfo."""
        column_names = []
        column_dtypes = []
        n_possible_values = []
        for column in dataset_info.columns:
            column_names.append(column.name)
            column_dtypes.append(column.data_type.name)
            n_possible_values.append(
                len(column.possible_values)
                if column.possible_values is not None
                else '-')
        return pd.DataFrame({
            'column': column_names,
            'dtype': column_dtypes,
            'count(possible_values)': n_possible_values
        })

    def __repr__(self):
        column_info = textwrap.indent(
            repr(self.get_summary_dataframe(self)), '    ')
        return (
            f'DatasetInfo:\n'
            f'  display_name: {self.display_name}\n'
            f'  files: {self.files}\n'
            f'  columns:\n'
            f'{column_info}'
        )

    def _col_id_from_name(self, name):
        """Look up the index of the column by name"""
        for i, c in enumerate(self.columns):
            if c.name == name:
                return i
        raise KeyError(name)

    def __getitem__(self, item):
        return self.columns[self._col_id_from_name(item)]

    def __setitem__(self, key, value):
        assert isinstance(value, Column), 'Must set column to be a ' \
                                          '`Column` object'
        self.columns[self._col_id_from_name(key)] = value

    def __delitem__(self, key):
        del self.columns[self._col_id_from_name(key)]


class ModelInfo:
    """Information about a model. Stored in `model.yaml` file on the backend.

    :param display_name: A name for user-facing display (different from an id).
    :param input_type: Specifies whether the model is in the tabular or text
        paradigm.
    :param model_task: Specifies the task the model is designed to address.
    :param inputs: A list of Column objects corresponding to the dataset
        columns that are fed as inputs into the model.
    :param outputs: A list of Column objects corresponding to the table
        output by the model when running predictions.
    :param targets: A list of Column objects corresponding to the dataset
        columns used as targets/labels for the model. If not provided, some
        functionality (like scoring) will not be available.
    :param framework: A string providing information about the software library
        and version used to train and run this model.
    :param description: A user-facing description of the model.
    :param **kwargs: Additional information about the model to store as `misc`.
    """

    def __init__(self, display_name: str, input_type: ModelInputType,
                 model_task: ModelTask, inputs: List[Column],
                 outputs: List[Column],
                 targets: Optional[List[Column]] = None,
                 framework: Optional[str] = None,
                 description: Optional[str] = None, **kwargs):
        self.display_name = display_name
        self.input_type = input_type
        self.model_task = model_task
        self.inputs = inputs
        self.outputs = outputs
        self.targets = targets
        self.framework = framework
        self.description = description
        self.misc = kwargs

    def to_dict(self):
        """Dumps to basic python objects (easy for JSON serialization)"""
        res = {
            'name': self.display_name,
            'input-type': self.input_type.value,
            'model-task': self.model_task.value,
            'inputs': [c.to_dict() for c in self.inputs],
            'outputs': [c.to_dict() for c in self.outputs],
        }
        if self.targets is not None:
            res['targets'] = self.targets
        if self.description is not None:
            res['description'] = self.description
        if self.framework is not None:
            res['framework'] = self.framework
        return {**res, **self.misc}

    def get_input_names(self):
        """Returns a list of names for model inputs."""
        return [column.name for column in self.inputs]

    def get_output_names(self):
        """Returns a list of names for model outputs."""
        return [column.name for column in self.outputs]

    @classmethod
    def from_dict(cls, deserialized_json: dict):
        """Transforms deserialized JSON into a ModelInfo object"""
        # drop down into the "model" object inside the deserialized_json
        deserialized_json = deserialized_json['model']

        name = deserialized_json.pop('name')
        input_type = ModelInputType(deserialized_json.pop('input-type'))
        model_task = ModelTask(deserialized_json.pop('model-task'))
        inputs = [Column.from_dict(c)
                  for c in deserialized_json.pop('inputs')]
        outputs = [Column.from_dict(c)
                   for c in deserialized_json.pop('outputs')]
        description = deserialized_json.pop('description', None)

        # instantiate the class
        return cls(
            name=name, input_type=input_type, model_task=model_task,
            inputs=inputs, outputs=outputs, description=description,
            **deserialized_json
        )

    @classmethod
    def from_dataset_info(
            cls,
            dataset_info: DatasetInfo,
            target: str,
            features: Sequence[str],
            display_name: Optional[str] = None,
            description: Optional[str] = None,
            input_type: ModelInputType = ModelInputType.TABULAR,
            model_task: Optional[ModelTask] = None,
    ):
        """Produces a ModelInfo for a model trained on a dataset.

        :param dataset_info: A DatasetInfo object describing the training
            dataset.
        :param target: The column name of the target the model predicts.
        :param features: A list of column names for columns used as features.
        :param display_name: A model name for user-facing display (different
            from an id).
        :param description: A user-facing description of the model.
        :param input_type: Specifies the paradigm (tabular or text) of the
            model.
        :param model_task: Specifies the prediction task addressed by the
            model. If not explicitly provided, this will be inferred from the
            data type of the target variable.

        :returns A ModelInfo object.
        """
        if display_name is None:
            display_name = f'{dataset_info.display_name} model'

        # infer inputs
        inputs = list()
        for column in dataset_info.columns:
            if (column.name != target and
                    (features is None or column.name in features)):
                inputs.append(
                    Column(name=column.name,
                           data_type=column.data_type,
                           possible_values=column.possible_values)
                )

        # determine target column
        try:
            target_column = dataset_info[target]
        except KeyError:
            raise ValueError(f'Target "{target}" not found in dataset.')

        # infer task type, outputs, and target levels from target
        if target_column.data_type.value == DataType.BOOLEAN.value:
            target_levels = [False, True]
            outputs = [
                Column(name=f'probability_{target_column.name}_True',
                       data_type=DataType.FLOAT)
            ]
            if model_task is None:
                model_task = ModelTask.BINARY_CLASSIFICATION
        elif target_column.data_type.value == DataType.CATEGORY.value:
            target_levels = target_column.possible_values
            if model_task is None:
                if len(target_levels) == 2:
                    model_task = ModelTask.BINARY_CLASSIFICATION
                else:
                    model_task = ModelTask.MULTICLASS_CLASSIFICATION
            if model_task.value == ModelTask.BINARY_CLASSIFICATION.value:
                outputs = [
                    Column(name=f'probability_{target_levels[1]}',
                           data_type=DataType.FLOAT)
                ]
            else:
                outputs = [
                    Column(name=f'probability_{level}',
                           data_type=DataType.FLOAT)
                    for level in target_levels
                ]
        else:
            target_levels = None
            outputs = [
                Column(name=f'predicted_{target_column.name}',
                       data_type=DataType.FLOAT)
            ]
            if model_task is None:
                model_task = ModelTask.REGRESSION

        return cls(
            display_name=display_name,
            description=description,
            input_type=input_type,
            model_task=model_task,
            inputs=inputs,
            outputs=outputs,
            targets=target_levels
        )

    @staticmethod
    def get_summary_dataframe(model_info):
        """Returns a table (pandas DataFrame) summarizing the ModelInfo."""
        column_names = []
        column_types = []
        column_dtypes = []
        n_possible_values = []
        for i, column in enumerate(model_info.inputs + model_info.outputs):
            column_names.append(column.name)
            column_type = 'input' if i < len(model_info.inputs) else 'output'
            column_types.append(column_type)
            column_dtypes.append(column.data_type.name)
            n_possible_values.append(
                len(column.possible_values)
                if column.possible_values is not None
                else '-')
        return pd.DataFrame({
            'column': column_names,
            'column_type': column_types,
            'dtype': column_dtypes,
            'count(possible_values)': n_possible_values
        })

    def __repr__(self):
        column_info = textwrap.indent(
            repr(self.get_summary_dataframe(self)), '    ')
        target_info = (f'  targets: {self.targets}\n'
                       if self.targets is not None
                       else '')
        framework_info = (f'  framework: {self.framework}\n'
                          if self.framework is not None
                          else '')
        misc_info = textwrap.indent(
            json.dumps(self.misc, indent=2), '    ')
        return (
            f'ModelInfo:\n'
            f'  display_name: {self.display_name}\n'
            f'  description: {self.description}\n'
            f'  input_type: {self.input_type}\n'
            f'  model_task: {self.model_task}\n'
            f'  inputs and outputs:\n'
            f'{column_info}\n'
            f'{target_info}'
            f'{framework_info}'
            f'  misc:\n'
            f'{misc_info}'
        )
