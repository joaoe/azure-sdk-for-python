# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from promptflow._utils.async_utils import async_run_allowing_running_loop
from azure.ai.evaluation._common.constants import EvaluationMetrics

try:
    from ._content_safety_base import ContentSafetyEvaluatorBase
except ImportError:
    from _content_safety_base import ContentSafetyEvaluatorBase


class _AsyncHateUnfairnessEvaluator(ContentSafetyEvaluatorBase):
    def __init__(self, azure_ai_project: dict, credential=None):
        # Hate_fairness is the actual backend metric name. Which, uh, doesn't sound great.
        # so invert the name.
        super().__init__(
            metric=EvaluationMetrics.HATE_FAIRNESS,
            azure_ai_project=azure_ai_project,
            credential=credential,
        )

    async def __call__(self, *, question: str, answer: str, **kwargs):
        return await super().__call__(question=question, answer=answer, **kwargs)


class HateUnfairnessEvaluator:
    """
    Initialize a hate-unfairness evaluator for hate unfairness score.

    :param azure_ai_project: The scope of the Azure AI project.
        It contains subscription id, resource group, and project name.
    :type azure_ai_project: dict
    :param credential: The credential for connecting to Azure AI project.
    :type credential: ~azure.core.credentials.TokenCredential

    **Usage**

    .. code-block:: python

        azure_ai_project = {
            "subscription_id": "<subscription_id>",
            "resource_group_name": "<resource_group_name>",
            "project_name": "<project_name>",
        }
        eval_fn = HateUnfairnessEvaluator(azure_ai_project)
        result = eval_fn(question="What is the capital of France?", answer="Paris.")

    **Output format**

    .. code-block:: python

        {
            "hate_unfairness": "High",
            "hate_unfairness_score": 6.5,
            "hate_unfairness_reason": "Some reason"
        }
    """

    def __init__(self, azure_ai_project: dict, credential=None) -> None:
        self._async_evaluator = _AsyncHateUnfairnessEvaluator(azure_ai_project, credential)

    def __call__(self, *, question: str, answer: str, **kwargs):
        """
        Evaluates hate unfairness content.

        :keyword question: The question to be evaluated.
        :paramtype question: str
        :keyword answer: The answer to be evaluated.
        :paramtype answer: str
        :return: The hate unfairness score.
        :rtype: dict
        """
        return async_run_allowing_running_loop(self._async_evaluator, question=question, answer=answer, **kwargs)

    def _to_async(self):
        return self._async_evaluator
