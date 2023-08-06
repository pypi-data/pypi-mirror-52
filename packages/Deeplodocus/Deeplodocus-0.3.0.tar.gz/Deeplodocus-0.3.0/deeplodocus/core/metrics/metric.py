import inspect
from typing import Union
import torch.nn as nn

from deeplodocus.flags import DEEP_NOTIF_FATAL
from deeplodocus.flags.entry import *
from deeplodocus.utils.notification import Notification
from deeplodocus.core.metrics.generic_metric import GenericMetric


class Metric(GenericMetric):
    """
    AUTHORS:
    --------

    :author: Alix Leroy

    DESCRIPTION:
    ------------

    A class which contains any metric to be computed

    """
    def __init__(self, name: str, method: Union[callable, nn.Module]):
        """
        AUTHORS:
        --------

        :author: Alix Leroy

        DESCRIPTION:
        ------------

        Initialize a Metric instance

        PARAMETERS:
        -----------

        :param name->str: The name of the metric
        :param method->Union[callable, torch.nn.Module]: The method to be computed

        RETURN:
        -------

        :return: None
        """
        super().__init__(name=name, method=method)
        self.method = self.__check_method(method)
        self.arguments = self.__check_arguments(method)

    @staticmethod
    def __check_method(method: Union[callable, nn.Module])->callable:
        """
        AUTHORS:
        --------

        :author: Alix Leroy

        DESCRIPTION:
        ------------

        Check if the method is a PyTorch Module or not

        PARAMETERS:
        -----------

        :param method->Union[callable, Module]: The method to be computed

        RETURN:
        -------

        :return: The method to be computed
        """
        if isinstance(method, nn.Module):
            return method.forward
        else:
            return method

    @staticmethod
    def is_loss():
        """
        AUTHORS:
        --------

        :author: Alix Leroy

        DESCRIPTION:
        ------------

        Check if the GenericMetric uses a loss function or not

        PARAMETERS:
        -----------

        None

        RETURN:
        -------
        :return->bool: False
        """
        return False

    def __check_arguments(self, method: Union[callable, nn.Module])-> list:
        """
        AUTHORS:
        --------

        :author: Alix Leroy

        DESCRIPTION:
        ------------

        Check what arguments are required in the method

        PARAMETERS:
        -----------

        :param method->Union[callable, Module]: The method to analyze

        RETURN:
        -------

        :return arguments->list: The list of arguments (DEEP flags)
        """

        arguments = []

        if isinstance(method, nn.Module):
            arguments_list = inspect.getfullargspec(method.forward)[0]
        elif inspect.isclass(method):
            # TODO for metric as a new class
            pass
        else:
            try:
                arguments_list = inspect.getfullargspec(method)[0]
            except TypeError as e:
                Notification(
                    DEEP_NOTIF_FATAL,
                    "Could not load metric : " + str(e).capitalize(),
                    solutions=["Ensure module and name are specified correctly in config/metrics",
                               "If using a custom metric, ensure it is defined correctly"]
                )

        input_list= ["input", "x", "inputs"]
        output_list = ["out", "y_pred", "y_predicted", "output", "outputs"]
        label_list = ["y", "y_expect", "y_expected", "label", "labels", "target", "targets"]
        additional_data_list = ["additional_data", "aditional_data"]

        for arg in arguments_list:
            if arg in input_list:
                if isinstance(method, nn.Module):
                    arguments.append(DEEP_ENTRY_OUTPUT)
                else:
                    arguments.append(DEEP_ENTRY_INPUT)
            elif arg in output_list:
                arguments.append(DEEP_ENTRY_OUTPUT)
            elif arg in label_list:
                arguments.append(DEEP_ENTRY_LABEL)
            elif arg in additional_data_list:
                arguments.append(DEEP_ENTRY_ADDITIONAL_DATA)
            elif arg == "self":
                continue
            else:
                Notification(DEEP_NOTIF_FATAL, "The following argument is not handled by the Deeplodocus metric system, please check the documentation : " + str(arg))
        return arguments
