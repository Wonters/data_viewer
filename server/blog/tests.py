from django.test import TestCase
from .tasks import create_dataset

class CeleryTestCase(TestCase):

    def test_create_dataset_task(self):
        # Appeler la tâche avec un argument
        result = create_dataset.delay(3)

        # Vérifiez que le résultat est ce que vous attendez
        # Dans ce cas, on n'attend pas vraiment de retour spécifique, mais vous pouvez
        # l'adapter en fonction de ce que votre tâche retourne.
        self.assertEqual(result.result, 3)
