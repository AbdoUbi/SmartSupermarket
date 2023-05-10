from subprocess import call


def facial_recognition():
    call(
        [
            "python",
            "./INFRONT OF THE SUPERMARKET/Facial Recognition Py/Facial Recognition.py",
        ]
    )


def SensorFusion():
    call(["python", "./INSIDE THE SUPERMARKET/SP SENSOR FUSION/SensorFusion.py"])


def FinalCalculator():
    call(["python", "./INSIDE THE SUPERMARKET/SP SHOPPING CART/FinalCalculator.py"])


facial_recognition()
SensorFusion()
FinalCalculator()
