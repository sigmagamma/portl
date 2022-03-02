import unittest
from file_tools import FileTools,steam_path_windows
from text_tools import rearrange_multiple_lines
ft = FileTools("The Stanley Parable", steam_path_windows(), "hebrew")
def normalize(st):
    return st.replace(" ","").replace("<cr>","")
class TestTextTools(unittest.TestCase):
    def test_regular(self):
        test_string = "זהו סיפורו של אדם בשם סטנלי."
        comparison_string = normalize(".ילנטס םשב םדא לש ורופיס והז <cr>")
        self.assertEqual(comparison_string,normalize(rearrange_multiple_lines(test_string,ft.max_chars_before_break,None)))

    def test_number(self):
        test_string = "תפקידו של עובד מספר 427 היה פשוט: הוא ישב על יד שולחנו בחדר 427 והקיש על מקשים במקלדת."
        comparison_string = normalize(":טושפ היה 427 רפסמ דבוע לש ודיקפת <cr>לע שיקהו 427 רדחב ונחלוש די לע בשי אוה <cr>.תדלקמב םישקמ <cr>")
        self.assertEqual(comparison_string,normalize(rearrange_multiple_lines(test_string,ft.max_chars_before_break,None)))
    def test_number_period(self):
        test_string = "סטנלי עבד בחברה בבניין גדול שם היה הוא עובד מספר 427."
        comparison_string = normalize("היה םש לודג ןיינבב הרבחב דבע ילנטס <cr>.427 רפסמ דבוע אוה <cr>")
        self.assertEqual(comparison_string,normalize(rearrange_multiple_lines(test_string,ft.max_chars_before_break,None)))
    def test_number_dashes(self):
        test_string = "ולהם הקצה הבוס ססמה סודית: 2-8-4-5"
        comparison_string = normalize("2-8-4-5 :תידוס המסס סובה הצקה םהלו <cr>")
        self.assertEqual(comparison_string,normalize(rearrange_multiple_lines(test_string,ft.max_chars_before_break,None)))
    def test_number_dashes(self):
        test_string = "ולהם הקצה הבוס ססמה סודית: 2-8-4-5"
        comparison_string = normalize("2-8-4-5 :תידוס המסס סובה הצקה םהלו <cr>")
        self.assertEqual(comparison_string,normalize(rearrange_multiple_lines(test_string,ft.max_chars_before_break,None)))

    def test_number_dashes_period(self):
        test_string = "2-8-4-5."
        comparison_string = normalize(".2-8-4-5")
        self.assertEqual(comparison_string,normalize(rearrange_multiple_lines(test_string,ft.max_chars_before_break,None)))

    def test_len(self):
        test_string = "<len:3>וסטנלי היה מאושר."
        comparison_string = normalize(".רשואמ היה <len:3>ילנטסו <cr>")
        self.assertEqual(comparison_string,normalize(rearrange_multiple_lines(test_string,ft.max_chars_before_break,None)))

    def test_reddoor(self):
        test_string = "אני עדיין מרגיש שיש בינינו קצר בתקשורת. סטנלי עבר בדלת <clr:255,0,0>האדומה<clr:255,255,255>."
        comparison_string = normalize("רצק וניניב שיש שיגרמ ןיידע ינא <cr>תלדב רבע ילנטס .תרושקתב <cr><clr:255,0,0>המודאה<clr:255,255,255>. <cr>")
        self.assertEqual(comparison_string,normalize(rearrange_multiple_lines(test_string,ft.max_chars_before_break,None)))

if __name__ == '__main__':
    unittest.main()
