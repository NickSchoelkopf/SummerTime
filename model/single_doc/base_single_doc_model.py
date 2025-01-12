from model.base_model import SummModel


class SingleDocSummModel(SummModel):
    def __init__(
        self,
        trained_domain: str = None,
        max_input_length: int = None,
        max_output_length: int = None,
    ):
        super(SingleDocSummModel, self).__init__(
            trained_domain=trained_domain,
            max_input_length=max_input_length,
            max_output_length=max_output_length,
        )

    @classmethod
    def assert_summ_input_type(cls, corpus, query):
        if not isinstance(corpus, list):
            raise TypeError(
                "Single-document summarization requires corpus of `List[str]`."
            )
        if not all([isinstance(ins, str) for ins in corpus]):
            raise TypeError(
                "Single-document summarization requires corpus of `List[str]`."
            )

        if query is not None:
            if not isinstance(query, list):
                raise TypeError(
                    "Query-based single-document summarization requires query of `List[str]`."
                )
            if not all([isinstance(q, str) for q in query]):
                raise TypeError(
                    "Query-based single-document summarization requires query of `List[str]`."
                )
