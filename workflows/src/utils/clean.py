from typing import Tuple
def clean_gather_results(results) -> Tuple[list, list]:
    """
    Extract failed index and clean the results
    :param results:
    :return:
    """
    # extract failed tasks to retrieve indexes
    failed = [
        index for index, result in enumerate(results) if isinstance(result, Exception)
    ]
    return failed, [result for result in results if not isinstance(result, Exception)]