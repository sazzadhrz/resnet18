# triton_python_backend_utils is available in every Triton Python model. You
# need to use this module to create inference requests and responses. It also
# contains some utility functions for extracting information from model_config
# and converting Triton input/output types to numpy types.
import triton_python_backend_utils as pb_utils
import json


class TritonPythonModel:
    """Your Python model must use the same class name. Every Python model
    that is created must have "TritonPythonModel" as the class name.
    """

    def initialize(self, args):
        """`initialize` is called only once when the model is being loaded.
        Implementing `initialize` function is optional. This function allows
        the model to intialize any state associated with this model.
        Parameters
        ----------
        args : dict
          Both keys and values are strings. The dictionary keys and values are:
          * model_config: A JSON string containing the model configuration
          * model_instance_kind: A string containing model instance kind
          * model_instance_device_id: A string containing model instance device ID
          * model_repository: Model repository path
          * model_version: Model version
          * model_name: Model name
        """

        # You must parse model_config. JSON string is not parsed here
        self.model_config = json.loads(args['model_config'])

    
    def execute(self, requests):
        """`execute` must be implemented in every Python model. `execute`
        function receives a list of pb_utils.InferenceRequest as the only
        argument. This function is called when an inference request is made
        for this model. Depending on the batching configuration (e.g. Dynamic
        Batching) used, `requests` may contain multiple requests. Every
        Python model, must create one pb_utils.InferenceResponse for every
        pb_utils.InferenceRequest in `requests`. If there is an error, you can
        set the error argument when creating a pb_utils.InferenceResponse
        Parameters
        ----------
        requests : list
        A list of pb_utils.InferenceRequest
        Returns
        -------
        list
        A list of pb_utils.InferenceResponse. The length of this list must
        be the same as `requests`
        """

        responses = []
        # Every Python backend must iterate over everyone of the requests
        # and create a pb_utils.InferenceResponse for each of them.
        for request in requests:
            # Get INPUT0
            in_0 = pb_utils.get_input_tensor_by_name(request, "INPUT0")

            # # Get INPUT1
            # in_1 = pb_utils.get_input_tensor_by_name(request, "INPUT1")

            # Get Model Name
            model_name = pb_utils.get_input_tensor_by_name(
                request, "MODEL_NAME")

            # Model Name string
            model_name_string = model_name.as_numpy()[0]

            # Create inference request object
            infer_request = pb_utils.InferenceRequest(
                model_name=model_name_string,
                # requested_output_names=["OUTPUT0", "OUTPUT1"],
                requested_output_names=["OUTPUT0"],
                inputs=[in_0])

            # print('Infer Request - ', infer_request)

            infer_response = infer_request.exec()
            print(in_0.shape)
            print(infer_response.output_tensors())

            if infer_response.has_error():
                raise pb_utils.TritonModelException(
                    infer_response.error().message())

            inference_response = pb_utils.InferenceResponse(
                output_tensors=infer_response.output_tensors())
            responses.append(inference_response)

        return responses

    def finalize(self):
        """`finalize` is called only once when the model is being unloaded.
        Implementing `finalize` function is OPTIONAL. This function allows
        the model to perform any necessary clean ups before exit.
        """
        print('Cleaning up...')