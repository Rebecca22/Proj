__author__ = "Rebecca Merriman"
import unittest
from src.SystemCallRepresentation import SystemCallRepresentation
from src.JsonFiles import ReadFromJsonFiles


class TestSystemCallRepresentation(unittest.TestCase):
    """
        This class is the Unit Test class for the SystemCallRepresentation class.
    """

    # Tests
    # Test 10 tests getSystemCallRepresentation() function in the SystemCallRepresentation class.
    # Test 12 tests get getAllSystemCallNames() function in the SystemCallRepresentation class.
    # Test 20 tests get getAllSamplesIds() function in the SystemCallRepresentation class.

    def testGetSystemCallRepresentation(self):
        """
         Test 10
           This method tests getSystemCallRepresentation() function in the SystemCallRepresentation
           class.
           To pass the test, the method SystemCallRepresentation() should  distinguish
           between ioctl and syscalls (if type = b or f) or distinguish between syscalls and binder
           transactions (if type = bb or fb) or distinguish between composite behaviours and ioctl(
           if type = bc or fc) or distinguish between composite behaviours and binder transactions
           and produce a list of syscalls and ioctl from the all files in all the families from the
           dictionary returned in the class ReadFromJsonFiles.
           Changes: I changed the getSystemCallRepresentation method to instead of returning a
           variable or a list or a list containing the first syscall from the first family or a list
           of all the syscalls in the first family or a list containing the syscalls and ioctls
           of the first family or a list containing the syscalls and ioctls from all
           the files from the first family, or a list containing the syscalls and ioctls from all
           the files from all families in the directory returned in the class ReadFromJsonFiles. I
           changed it to distinguish between the type of behaviour to represent. If the type = "b"
           or "f" it should represent the behaviours as syscalls and ioctl, if the type = "bb" or
           "fb" it should represent the behaviours as syscalls with binder semantics, if the type
           = "bc" or "fc" it should represent the behaviours as composite behaviours with ioctl and
           if the type = "bbc" or "fbc" it should represent the behaviours as composite behaviours
           with binder semantics. produceVector() method in ProduceVector class and tests in
           TestProduceVector class were  changed to incorporate the type of behaviour by adding
           another argument to the method signature when it calls getSystemCallRepresentation().
           Added behaviour types syscall and binder, composite and ioctl and composite and binder.
           :param self: reference to the current instance of the class
        """

        test = ['write', 'ioctl', 'connect', 'sendto', 'open', 'execve']
        setSyscalls = set(SystemCallRepresentation.getSystemCallRepresentation(typeSyscall="b"))
        setList = list(setSyscalls)
        self.assertEqual(setList, test,
                         "Test 10: Test getSystemCallRepresentation bit vector ")
        setSyscalls = set(SystemCallRepresentation.getSystemCallRepresentation(typeSyscall="f"))
        setList = list(setSyscalls)
        self.assertEqual(setList, test,
                         "Test 10: Test getSystemCallRepresentation freq vector")

        test = ['com.android.internal.telephony.ITelephony.TRANSACTION_getNetworkType()',
                'com.android.internal.telephony.IPhoneSubInfo.getVoiceMailNumber()()', 'connect',
                'com.android.internal.telephony.IPhoneSubInfo.getLine1Number()()', 'open',
                'com.android.internal.telephony.ISms.SMS_sendText()',
                'android.intent.action.PHONE_STATE',
                'com.android.internal.telephony.ITelephony'
                '.TRANSACTION_cancelMissedCallsNotification()',
                'android.accounts.IAccountManager.TRANSACTION_getAccountsByFeatures()',
                'android.location.ILocationManager.TRANSACTION_requestLocationUpdates()',
                'write', 'android.accounts.IAccountManager.TRANSACTION_getAccounts()',
                'com.android.internal.telephony.IPhoneSubInfo.getDeviceSvn()()',
                'android.location.ILocationManager.TRANSACTION_getAllProviders()',
                'com.android.internal.telephony.IPhoneSubInfo.getIccSerialNumber()()',
                'android.app.IActivityManager.GET_CONTENT_PROVIDER_TRANSACTION()',
                'com.android.internal.telephony.IPhoneSubInfo.getSubscriberId()()',
                'android.provider.Telephony.SMS_RECEIVED',
                'android.app.IActivityManager.START_ACTIVITY_TRANSACTION',
                'com.android.internal.telephony.ITelephony.TRANSACTION_getCellLocation()',
                'execve', 'android.location.ILocationManager.TRANSACTION_getProviderInfo()',
                'com.android.internal.telephony.ITelephony.TRANSACTION_getActivePhoneType()',
                'com.android.internal.telephony.IPhoneSubInfo.getDeviceId()()', 'sendto',
                'android.location.ILocationManager.TRANSACTION_getLastKnownLocation()',
                'android.location.ILocationManager.TRANSACTION_getProviders()']

        setSyscalls = set(SystemCallRepresentation.getSystemCallRepresentation(typeSyscall="bb"))
        setList = list(setSyscalls)
        self.assertEqual(setList, test,
                         "Test 10: Test getSystemCallRepresentation bit binder vector")
        setSyscalls = set(SystemCallRepresentation.getSystemCallRepresentation(typeSyscall="fb"))
        setList = list(setSyscalls)
        self.assertEqual(setList, test,
                         "Test 10: Test getSystemCallRepresentation freq binder vector")

        test = ['ioctl', 'FS ACCESS', 'NETWORK ACCESS', 'execve']

        setSyscalls = set(SystemCallRepresentation.getSystemCallRepresentation(typeSyscall="bc"))
        setList = list(setSyscalls)
        self.assertEqual(setList, test,
                         "Test 10: Test getSystemCallRepresentation bit composite vector")

        setSyscalls = set(SystemCallRepresentation.getSystemCallRepresentation(typeSyscall="fc"))
        setList = list(setSyscalls)
        self.assertEqual(setList, test,
                         "Test 10: Test getSystemCallRepresentation frequency composite vector")

    def testGetAllSystemCallNames(self):
        """
         Test 12
           This method tests getAllSystemCallNames() function in the SystemCallRepresentation
           class.
           To pass the test, the method getAllSystemCallNames() should return the correct
           SystemCallNames accordingly.
           :param self: reference to the current instance of the class
        """
        ReadFromJsonFiles.readJsonFile()
        syscalls = [set(SystemCallRepresentation.getSystemCallRepresentation("b"))]

        syscallNames = SystemCallRepresentation.getAllSystemCallNames()
        listDictionary = {}

        for sample in range(0, len(syscallNames)):
            for index in range(0, len(syscallNames[sample])):
                names = syscallNames[sample][index]
                for index2 in range(0, len(names)):
                    key = names[index2]
                    if key not in listDictionary:
                        listDictionary[key] = 0
        dictionary = {}
        for index in range(0, len(syscalls)):
            values = syscalls[index]
            for index2 in range(0, len(values)):
                dictionary[values.pop()] = 0

        listKeys = dictionary.keys()
        listNames = listDictionary.keys()

        self.assertEqual(listNames, listKeys, "Test 12: Test getAllSystemCallNames")

    def getAllSamplesIds(self):
        """
         Test 20
           This method tests getAllSamplesIds() function in the SystemCallRepresentation
           class.
           To pass the test, the method getAllSamplesIds() should return dictionary of all the id's
           of each file in each family
           Changes: Added getAllSamplesIds to produce vector and TestProduceVector (was referring to
           the variable int in the class without a getter before.
           :param self: reference to the current instance of the class
        """
        ReadFromJsonFiles.readJsonFile()
        syscalls = [set(SystemCallRepresentation.getSystemCallRepresentation("b"))]

        syscallIds = SystemCallRepresentation.getAllSamplesIds()
        listDictionary = {}
        for index in range(0, len(syscallIds)):
            ids = syscallIds[index]
            for index2 in range(0, len(ids)):
                key = ids[index2]
                if key not in listDictionary:
                    listDictionary[key] = 0
        dictionary = {}
        for index in range(0, len(syscalls)):
            values = syscalls[index]
            for index2 in range(0, len(values)):
                dictionary[values.pop()] = 0

        listKeys = dictionary.keys()
        listIds = listDictionary.keys()

        self.assertEqual(listIds, listKeys, "Test 20: Test getAllSamplesIds")


if __name__ == '__main__':
    unittest.main()
