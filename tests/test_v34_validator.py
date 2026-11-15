#!/usr/bin/env python3
"""validate_scenario_json.py, 3.4: the regulated-flow reading (item 35), refusal messages that carry the
corrected value (item 8) and the mechanical checks moved over from scenario-critic (item 7). Stdlib only.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import validate_scenario_json as vsj  # noqa: E402
from test_validate_scenario_json_v3 import plain, with_b, errs, warns, has  # noqa: E402

REGULATION = {"type": "regulation", "text": "B’nin metni için uyum onayı alınmadan teste trafik açılmaz."}


def grocery(**changes):
    """A grocery cart record: the words a checkout uses for confirming an order, nothing legally bound."""
    sc = plain(stage="cart-checkout", title="Sepet özetini onay ekranından önce göstermek siparişi artırır mı?",
               problem="Market sepetinde sipariş özeti yalnızca onay ekranında görünüyor.",
               mechanism="Özet onay ekranından önce görününce kullanıcı Siparişi onayla adımına tutarı bilerek gelir.")
    sc.update(changes)
    return sc


class TestRegulatedFlowReading(unittest.TestCase):
    """Item 35: "onay" counts only in its consent sense; a confirmation screen is no regulated flow."""

    def test_order_confirmation_words_are_not_regulated(self):
        for text in ("Market sepetinde onay ekranı tutarı gösteriyor.", "Siparişi onayla butonu altta duruyor.",
                     "Sipariş onayı e-postası gecikiyor.", "Onay kutusu formun sonunda duruyor.",
                     "The order confirmation screen shows the total."):
            sc = grocery(problem=text)
            self.assertFalse(has(errs(sc), "regulated flow"), (text, errs(sc)))
        self.assertEqual(errs(grocery()), [])

    def test_consent_sense_is_still_regulated(self):
        for text, word in (("Kayıt formundaki pazarlama onayı kutusu uzun.", "pazarlama onayı"),
                           ("Ticari ileti onayı metni kısalıyor.", "ileti onayı"),
                           ("Açık rıza metni adımın sonunda duruyor.", "rıza"),
                           ("KVKK onayı alanın altında duruyor.", "KVKK"),
                           ("Onay metni iki satıra iniyor.", "Onay metni"),
                           ("The consent box sits under the field.", "consent")):
            sc = grocery(problem=text)
            self.assertTrue(has(errs(sc), "regulated flow (%s" % word), (text, errs(sc)))
            sc["warnings"] = [REGULATION]
            self.assertFalse(has(errs(sc), "regulated flow"), (text, errs(sc)))

    def test_subscription_cancellation_and_data_purpose_copy_are_regulated(self):
        for text in ("Abonelik iptali ekranında dondurma seçeneği yok.", "Aboneliği iptal eden kullanıcı geri dönemiyor.",
                     "Users who cancel their subscription see no pause option.",
                     "B adds “No spam, unsubscribe anytime” under the email field.",
                     "Kişisel veri kullanımını anlatan satır butonun altında.", "Gizlilik notu butonun altında.",
                     "A privacy note sits below the button."):
            sc = with_b(plain(), text)
            self.assertTrue(has(errs(sc), "regulated flow"), (text, errs(sc)))

    def test_order_cancellation_is_not_a_subscription(self):
        sc = with_b(plain(), "Sipariş iptal bağlantısı özetin altında")
        sc["warnings"] = [{"type": "accessibility", "text": ("Bağlantı klavyeyle erişilebilir, ekran okuyucuda adıyla "
                                                             "okunur, dokunma alanı en az 44×44 pt ve kontrastı en az "
                                                             "4.5:1 olmalı.")}]
        sc["invariants"] = ["Bağlantı iki kolda da aynı iptal adımını açar."]
        self.assertFalse(has(errs(sc), "regulated flow"), errs(sc))


if __name__ == "__main__":
    unittest.main()
