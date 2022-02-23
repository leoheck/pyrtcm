"""
Stream method tests using actual receiver binary outputs for pyrtcm.rtcmReader 

Created on 3 Oct 2020 

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""
# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest

from pyrtcm import RTCMReader, RTCMMessage
import pyrtcm.exceptions as rte
import pyrtcm.rtcmtypes_core as rtt


class StreamTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)
        self._raw1005ex = b"\xD3\x00\x13\x3E\xD7\xD3\x02\x02\x98\x0E\xDE\xEF\x34\xB4\xBD\x62\xAC\x09\x41\x98\x6F\x33\x36\x0B\x98"
        self._raw1005 = (
            b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
        )
        self._raw1007 = b"\xd3\x00\x08>\xf4\xd2\x03ABC\xeapo\xc7"
        # 00111110 11110100 11010010 00000011 01000001 01000010 01000011 11101010
        self._raw1065 = (
            b"\xd3\x00\x12B\x91\x81\xc9\x84\x00\x04B\xb8\x88\x008\x80\t\xd0F\x00(\xf0kf"
        )
        self._payload1007 = self._raw1007[3:-3]

    def tearDown(self):
        pass

    def test1005example(
        self,
    ):  # test sample 1005 given in RTCM standard (with scaling applied)
        EXPECTED_RESULT = "<RTCM(1005, DF002=1005, DF003=2003, DF021=0, DF022=1, DF023=0, DF024=0, DF141=0, DF025=1114104.5999, DF142=0, DF001_1=0, DF026=-4850729.7108, DF364=0, DF027=3975521.4643)>"
        msg = RTCMReader.parse(self._raw1005ex, scaling=True)
        self.assertEqual(str(msg), EXPECTED_RESULT)
        self.assertEqual(msg.DF025, 1114104.5999)
        self.assertEqual(msg.DF026, -4850729.7108)
        self.assertEqual(msg.DF027, 3975521.4643)

    def testMIXEDRTCM(
        self,
    ):  # test mixed stream of NMEA, UBX & RTCM messages TODO when fully implemented
        EXPECTED_RESULTS = (
            "<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=44440308028, DF142=1, DF001_1=0, DF026=30856712349, DF364=0, DF027=33666582560)>",
            "<RTCM(4072, DF002=4072, Not_Yet_Implemented)>",
            "<RTCM(1077, DF002=1077, DF003=0, GNSSEpoch=204137001, DF393=1, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=760738918298550272, NSat=10, DF395=1073807360, NSig=2, DF396=1044459, DF405_01=308405, DF405_02=84035, DF405_03=328885, DF405_04=150343, DF405_05=0, DF405_06=0, DF405_07=6691, DF405_08=-248690, DF405_09=-471948, DF405_10=-205719, DF405_11=-501406, DF405_12=-11330, DF405_13=-192673, DF405_14=269791, DF405_15=-53208, DF405_16=329796, DF405_17=164857, DF405_18=343883, DF405_19=76821, DF405_20=76146, DF406_01=3335715, DF406_02=2913984, DF406_03=-6996952, DF406_04=-3723880, DF406_05=7457979, DF406_06=1848654, DF406_07=7644135, DF406_08=-184532, DF406_09=7533336, DF406_10=-3937275, DF406_11=3750797, DF406_12=7647703, DF406_13=-7651254, DF406_14=6950987, DF406_15=3055820, DF406_16=-5308213, DF406_17=2100994, DF406_18=646922, DF406_19=-8388426, DF406_20=2052210, DF407_01=81, DF407_02=263, DF407_03=78, DF407_04=927, DF407_05=632, DF407_06=728, DF407_07=999, DF407_08=970, DF407_09=959, DF407_10=185, DF407_11=731, DF407_12=973, DF407_13=14, DF407_14=13, DF407_15=540, DF407_16=64, DF407_17=913, DF407_18=527, DF407_19=983, DF407_20=206, DF420_01=0, DF420_02=0, DF420_03=0, DF420_04=0, DF420_05=1, DF420_06=1, DF420_07=1, DF420_08=1, DF420_09=0, DF420_10=1, DF420_11=0, DF420_12=1, DF420_13=1, DF420_14=1, DF420_15=1, DF420_16=0, DF420_17=0, DF420_18=0, DF420_19=0, DF420_20=0, DF408_01=29, DF408_02=341, DF408_03=341, DF408_04=341, DF408_05=341, DF408_06=341, DF408_07=341, DF408_08=341, DF408_09=341, DF408_10=341, DF408_11=341, DF408_12=341, DF408_13=341, DF408_14=341, DF408_15=157, DF408_16=341, DF408_17=341, DF408_18=340, DF408_19=0, DF408_20=22, DF404_01=-15776, DF404_02=-10733, DF404_03=-15760, DF404_04=-13802, DF404_05=-15648, DF404_06=-9197, DF404_07=-15840, DF404_08=-9709, DF404_09=496, DF404_10=-9705, DF404_11=656, DF404_12=-9231, DF404_13=-9194, DF404_14=-8321, DF404_15=-8326, DF404_16=-4107, DF404_17=-4072, DF404_18=2451, DF404_19=-693, DF404_20=-684)>",
            "<RTCM(1087, DF002=1087, DF003=0, GNSSEpoch=310554457, DF393=1, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=4039168114821169152, NSat=7, DF395=1090519040, NSig=2, DF396=16382, DF405_01=283652, DF405_02=-439230, DF405_03=287980, DF405_04=-162553, DF405_05=-351659, DF405_06=-48877, DF405_07=-97420, DF405_08=-7555, DF405_09=421895, DF405_10=272911, DF405_11=462834, DF405_12=-195360, DF405_13=81184, DF405_14=-330976, DF406_01=-1331299, DF406_02=-2033342, DF406_03=-5236897, DF406_04=184723, DF406_05=-2403522, DF406_06=-2540334, DF406_07=8048310, DF406_08=4343116, DF406_09=2466558, DF406_10=1102600, DF406_11=2876424, DF406_12=3647230, DF406_13=6976766, DF406_14=5381632, DF407_01=374, DF407_02=112, DF407_03=45, DF407_04=742, DF407_05=61, DF407_06=653, DF407_07=707, DF407_08=995, DF407_09=31, DF407_10=820, DF407_11=798, DF407_12=243, DF407_13=702, DF407_14=416, DF420_01=1, DF420_02=0, DF420_03=0, DF420_04=1, DF420_05=0, DF420_06=0, DF420_07=0, DF420_08=1, DF420_09=1, DF420_10=0, DF420_11=1, DF420_12=1, DF420_13=0, DF420_14=0, DF408_01=192, DF408_02=604, DF408_03=130, DF408_04=992, DF408_05=960, DF408_06=661, DF408_07=341, DF408_08=341, DF408_09=277, DF408_10=277, DF408_11=341, DF408_12=341, DF408_13=277, DF408_14=341, DF404_01=10922, DF404_02=-10923, DF404_03=10920, DF404_04=5, DF404_05=-3936, DF404_06=6021, DF404_07=8380, DF404_08=4996, DF404_09=-16252, DF404_10=6149, DF404_11=12480, DF404_12=5125, DF404_13=4287, DF404_14=-64)>",
            "<RTCM(1097, DF002=1097, DF003=0, GNSSEpoch=204137001, DF393=1, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=216181732825628672, NSat=5, DF395=1073872896, NSig=2, DF396=1023, DF405_01=324933, DF405_02=-438701, DF405_03=0, DF405_04=164097, DF405_05=372092, DF405_06=273395, DF405_07=-329744, DF405_08=108288, DF405_09=-384, DF405_10=-24373, DF406_01=-242675, DF406_02=2781653, DF406_03=2724848, DF406_04=-5553741, DF406_05=3072198, DF406_06=-1082673, DF406_07=-2534145, DF406_08=-6684696, DF406_09=-5074959, DF406_10=2252615, DF407_01=167, DF407_02=501, DF407_03=312, DF407_04=736, DF407_05=1010, DF407_06=930, DF407_07=65, DF407_08=662, DF407_09=318, DF407_10=893, DF420_01=1, DF420_02=1, DF420_03=1, DF420_04=1, DF420_05=1, DF420_06=0, DF420_07=1, DF420_08=0, DF420_09=1, DF420_10=1, DF408_01=957, DF408_02=771, DF408_03=255, DF408_04=418, DF408_05=783, DF408_06=1017, DF408_07=97, DF408_08=341, DF408_09=341, DF408_10=341, DF404_01=10922, DF404_02=-10923, DF404_03=10922, DF404_04=-10923, DF404_05=10912, DF404_06=736, DF404_07=-7660, DF404_08=-15696, DF404_09=-10731, DF404_10=-15664)>",
            "<RTCM(1127, DF002=1127, DF003=0, GNSSEpoch=204123001, DF393=0, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=198178247981137920, NSat=10, DF395=1074003968, NSig=2, DF396=387754, DF405_01=-518073, DF405_02=-111791, DF405_03=345316, DF405_04=-359850, DF405_05=0, DF405_06=0, DF405_07=123373, DF405_08=325351, DF405_09=430664, DF405_10=-461494, DF405_11=-441678, DF405_12=-8257, DF405_13=-233493, DF405_14=-261617, DF405_15=-407525, DF405_16=325591, DF405_17=-16387, DF405_18=163919, DF405_19=-208596, DF405_20=122033, DF406_01=3467427, DF406_02=4103914, DF406_03=2215836, DF406_04=4665386, DF406_05=3288696, DF406_06=-2149697, DF406_07=554457, DF406_08=8314676, DF406_09=7843958, DF406_10=-4235053, DF406_11=6574287, DF406_12=-2691160, DF406_13=7950310, DF406_14=-7069503, DF406_15=-2731893, DF406_16=2547580, DF406_17=5418945, DF406_18=-3747995, DF406_19=6002005, DF406_20=5592405, DF407_01=341, DF407_02=341, DF407_03=341, DF407_04=341, DF407_05=341, DF407_06=341, DF407_07=341, DF407_08=320, DF407_09=22, DF407_10=532, DF407_11=533, DF407_12=22, DF407_13=536, DF407_14=23, DF407_15=21, DF407_16=23, DF407_17=536, DF407_18=22, DF407_19=21, DF407_20=538, DF420_01=0, DF420_02=1, DF420_03=1, DF420_04=1, DF420_05=0, DF420_06=1, DF420_07=0, DF420_08=1, DF420_09=1, DF420_10=0, DF420_11=1, DF420_12=1, DF420_13=0, DF420_14=1, DF420_15=0, DF420_16=0, DF420_17=0, DF420_18=0, DF420_19=0, DF420_20=0, DF408_01=798, DF408_02=664, DF408_03=982, DF408_04=389, DF408_05=872, DF408_06=795, DF408_07=513, DF408_08=708, DF408_09=889, DF408_10=410, DF408_11=169, DF408_12=813, DF408_13=613, DF408_14=1002, DF408_15=0, DF408_16=0, DF408_17=0, DF408_18=0, DF408_19=0, DF408_20=0, DF404_01=0, DF404_02=0, DF404_03=0, DF404_04=0, DF404_05=0, DF404_06=0, DF404_07=0, DF404_08=0, DF404_09=0, DF404_10=0, DF404_11=0, DF404_12=0, DF404_13=0, DF404_14=0, DF404_15=0, DF404_16=0, DF404_17=0, DF404_18=0, DF404_19=0, DF404_20=0)>",
            "<RTCM(1230, DF002=1230, DF003=0, DF421=1, DF001_3=0, DF422=0, )>",  # TODO CHECK this may not be right
            "<RTCM(1007, DF002=1007, DF003=1234, DF029=3, DF030_01=A, DF030_02=B, DF030_03=C, DF031=234)>",
        )
        dirname = os.path.dirname(__file__)
        stream = open(os.path.join(dirname, "pygpsdata-RTCM3.log"), "rb")
        i = 0
        raw = 0
        rtr = RTCMReader(stream)
        for (raw, parsed) in rtr.iterate():
            if raw is not None:
                print(parsed)
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
        stream.close()

    def testSerialize(self):  # test serialize()
        payload = self._raw1005[3:-3]
        msg1 = RTCMReader.parse(self._raw1005)
        msg2 = RTCMMessage(payload=payload)
        res = msg1.serialize()
        self.assertEqual(res, self._raw1005)
        res1 = msg2.serialize()
        self.assertEqual(res, self._raw1005)

    def testsetattr(self):  # test immutability
        EXPECTED_ERROR = (
            "Object is immutable. Updates to DF002 not permitted after initialisation."
        )
        with self.assertRaisesRegex(rte.RTCMMessageError, EXPECTED_ERROR):
            msg = RTCMReader.parse(self._raw1005)
            msg.DF002 = 9999

    def testrepr(self):  # test repr, check eval recreates original object
        EXPECTED_RESULT = "RTCMMessage(payload=b'>\\xd0\\x00\\x03\\x8aX\\xd9I<\\x87/4\\x10\\x9d\\x07\\xd6\\xafH ')"
        msg1 = RTCMReader.parse(self._raw1005)
        self.assertEqual(repr(msg1), EXPECTED_RESULT)
        msg2 = eval(repr(msg1))
        self.assertEqual(str(msg1), str(msg2))

    def testpayload(self):  # test payload getter
        msg = RTCMReader.parse(self._raw1005)
        payload = self._raw1005[3:-3]
        self.assertEqual(msg.payload, payload)

    def testgroups(self):  # test message with repeating group (1007)
        EXPECTED_RESULT = "<RTCM(1007, DF002=1007, DF003=1234, DF029=3, DF030_01=A, DF030_02=B, DF030_03=C, DF031=234)>"
        msg1 = RTCMMessage(payload=self._payload1007)
        msg2 = RTCMReader.parse(self._raw1007)
        self.assertEqual(str(msg1), EXPECTED_RESULT)
        self.assertEqual(str(msg2), EXPECTED_RESULT)

    def testnestedgroups(self):  # test message with nested repeating group (1059, 1065)
        EXPECTED_RESULT = "<RTCM(1065, DF002=1065, DF386=12345, DF391=3, DF388=0, DF413=1, DF414=1, DF415=1, DF387=2, DF384_01=23, DF379_01=2, DF381_01_01=4, DF383_01_01=0.07, DF381_01_02=2, DF383_01_02=0.09, DF384_02=26, DF379_02=1, DF381_02_01=3, DF383_02_01=0.05)>"
        msg = RTCMReader.parse(self._raw1065, scaling=True)
        self.assertEqual(str(msg), EXPECTED_RESULT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
