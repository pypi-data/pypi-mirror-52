from django.shortcuts import reverse


class SimpleCrudAPITestCase(object):

    # Test settings
    DISABLE_DEFAULT_TESTS = False  # disable the default tests

    # Test Constants
    URL_NAMESPACE = None
    URL_NAME = None
    MODEL = None

    # Endpoint settings
    ACTIONS = [
        'list',
        'retrieve',
        'destroy',
        'create',
        'update',
        'partial_update',
    ]

    def check_configuration(self, method):

        # Make sure the class is setup correctly

        self.assertIsNotNone(
            self.URL_NAMESPACE,
            'Please specify the URL_NAMESPACE')
        self.assertIsNotNone(
            self.URL_NAME,
            'Please specify the URL_NAME')
        self.assertIsNotNone(
            self.MODEL,
            'Please specify the MODEL')
        # Check the options for ACTIONS
        for a in self.ACTIONS:
            self.assertIn(
                a,
                [
                    'list',
                    'retrieve',
                    'destroy',
                    'create',
                    'update',
                    'partial_update',
                ],
                '{} is not a valid action name'.format(a)
            )

        # Lastly check the method is allowed
        return method in self.ACTIONS

    def get_reversed_url(self, action, *args):
        if action in [
            'retrieve',
            'destroy',
            'update',
            'partial_update'
        ]:
            suffix = 'detail'
        else:
            suffix = 'list'

        url = '{}:{}-{}'.format(self.URL_NAMESPACE, self.URL_NAME, suffix)
        reversed_url = reverse(url, args=args)
        return reversed_url

    def create_test_object(self):
        """
        Creates a test object for the model viewset
        """
        return self.MODEL.objects.create(**self.get_model_payload())

    def get_model_payload(self):  # pragma: no cover
        raise NotImplementedError("This needs to be abstracted")

    def get_request_payload(self):  # pragma: no cover
        raise NotImplementedError("This needs to be abstracted")

    def get_request_headers(self):
        return {}

    # Test retrieve list
    def test_can_read_list(self):

        # Check if default tests are disabled
        if self.DISABLE_DEFAULT_TESTS:  # pragma: no cover
            return

        # - First check that the class is setup and assign the correct status
        status = 200 if self.check_configuration('list') else 405

        # get the URL
        url = self.get_reversed_url('list')

        # Make the request
        response = self.client.get(url, headers=self.get_request_headers())

        # Assert statuscode
        self.assertEqual(response.status_code, status)

    # Test retrieve detail
    def test_can_read_retrieve(self):

        # Check if default tests are disabled
        if self.DISABLE_DEFAULT_TESTS:  # pragma: no cover
            return

        # - First check that the class is setup and assign the correct status
        status = 200 if self.check_configuration('retrieve') else 405

        # Create the test object
        test_obj = self.create_test_object()

        # get the URL
        url = self.get_reversed_url('retrieve', test_obj.id)

        # Make the request
        response = self.client.get(url, headers=self.get_request_headers())

        # Assert statuscode
        self.assertEqual(response.status_code, status)

    # Test write create
    def test_can_write_create(self):

        # Check if default tests are disabled
        if self.DISABLE_DEFAULT_TESTS:  # pragma: no cover
            return

        # - First check that the class is setup and assign the correct status
        status = 201 if self.check_configuration('create') else 405

        # get the URL
        url = self.get_reversed_url('create')

        payload = self.get_request_payload()

        # Make the request
        response = self.client.post(url, headers=self.get_request_headers())

        # Assert statuscode
        self.assertEqual(response.status_code, status)

    # Test write update
    def test_can_write_update(self):

        # Check if default tests are disabled
        if self.DISABLE_DEFAULT_TESTS:  # pragma: no cover
            return

        # - First check that the class is setup and assign the correct status
        status = 200 if self.check_configuration('update') else 405

        # get the URL
        test_obj = self.create_test_object()
        url = self.get_reversed_url('update', test_obj.id)
        payload = self.get_request_payload()

        # Make the request
        response = self.client.put(url, headers=self.get_request_headers())

        # Assert statuscode
        self.assertEqual(response.status_code, status)

    # Test write partial_update
    def test_can_write_partial_update(self):

        # Check if default tests are disabled
        if self.DISABLE_DEFAULT_TESTS:  # pragma: no cover
            return

        # - First check that the class is setup and assign the correct status
        status = 200 if self.check_configuration('partial_update') else 405

        # get the URL
        test_obj = self.create_test_object()
        url = self.get_reversed_url('partial_update', test_obj.id)
        payload = self.get_request_payload()

        # Make the request
        response = self.client.patch(url, headers=self.get_request_headers())

        # Assert statuscode
        self.assertEqual(response.status_code, status)

    # Test write destroy
    def test_can_write_destroy(self):

        # Check if default tests are disabled
        if self.DISABLE_DEFAULT_TESTS:  # pragma: no cover
            return

        # - First check that the class is setup and assign the correct status
        status = 204 if self.check_configuration('destroy') else 405

        # get the URL
        test_obj = self.create_test_object()
        url = self.get_reversed_url('destroy', test_obj.id)
        payload = self.get_request_payload()

        # Make the request
        response = self.client.delete(url, headers=self.get_request_headers())

        # Assert statuscode
        self.assertEqual(response.status_code, status)
