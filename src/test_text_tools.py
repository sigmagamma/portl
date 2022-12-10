import unittest
from src.file_tools import FileTools
from text_tools import rearrange_multiple_lines
stanley_ft = FileTools("../gamefiles/stanley/The Stanley Parable RTL.json", "hebrew")
portal_ft = FileTools("../gamefiles/portal/Portal 2007.json", "hebrew")
def normalize(st):
    return st.replace(" ","").replace("<cr>","")

def normalize_and_rearrange(st,ft):
    return normalize(rearrange_multiple_lines(st, ft.max_chars_before_break, None))

class TestTextTools(unittest.TestCase):
    def test_stanley_regular(self):
        test_string = normalize_and_rearrange("זהו סיפורו של אדם בשם סטנלי.",stanley_ft)
        comparison_string = normalize(".ילנטס םשב םדא לש ורופיס והז <cr>")
        self.assertEqual(comparison_string, test_string)

    def test_stanley_number(self):
        test_string = normalize_and_rearrange("תפקידו של עובד מספר 427 היה פשוט: הוא ישב על יד שולחנו בחדר 427 והקיש על מקשים במקלדת.",stanley_ft)
        comparison_string = normalize(":טושפ היה 427 רפסמ דבוע לש ודיקפת <cr>לע שיקהו 427 רדחב ונחלוש די לע בשי אוה <cr>.תדלקמב םישקמ <cr>")
        self.assertEqual(comparison_string, test_string)
    def test_stanley_number_period(self):
        test_string = normalize_and_rearrange(
            "סטנלי עבד בחברה בבניין גדול שם היה הוא עובד מספר 427.", stanley_ft)
        comparison_string = normalize("היה םש לודג ןיינבב הרבחב דבע ילנטס <cr>.427 רפסמ דבוע אוה <cr>")
        self.assertEqual(comparison_string, test_string)
    def test_stanley_number_dashes(self):
        test_string = normalize_and_rearrange(
            "ולהם הקצה הבוס ססמה סודית: 2-8-4-5", stanley_ft)
        comparison_string = normalize("2-8-4-5 :תידוס המסס סובה הצקה םהלו <cr>")
        self.assertEqual(comparison_string, test_string)
    def test_stanley_number_dashes_period(self):
        test_string = normalize_and_rearrange(
            "2-8-4-5.", stanley_ft)
        comparison_string = normalize(".2-8-4-5")
        self.assertEqual(comparison_string, test_string)
    def test_stanley_len(self):
        test_string = normalize_and_rearrange(
            "<len:3>וסטנלי היה מאושר.", stanley_ft)
        comparison_string = normalize(".רשואמ היה <len:3>ילנטסו <cr>")
        self.assertEqual(comparison_string, test_string)
    def test_portal_teeth(self):
        test_string = normalize_and_rearrange("אנא קחי בחשבון כי טעם מורגש של דם אינו חלק מאף נוהל ניסוי אך הינו תופעת לוואי בלתי צפויה של רשת שחרור החומר, אשר עלולה, במקרים נדירים למחצה, לשחרר סתימות דנטליות, כתרים, אמייל השן, ושיניים באופן כללי.",portal_ft)
        comparison_string = normalize("ףאמ קלח וניא םד לש שגרומ םעט יכ ןובשחב יחק אנא <cr>תשר לש היופצ יתלב יאוול תעפות וניה ךא יוסינ להונ <cr>ררחשל ,הצחמל םירידנ םירקמב ,הלולע רשא ,רמוחה רורחש <cr>.יללכ ןפואב םיינישו ,ןשה ליימא ,םירתכ ,תוילטנד תומיתס <cr>")
        self.assertEqual(comparison_string, test_string)
    def test_portal_number(self):
        test_string = normalize_and_rearrange("כל טכנולוגיות אפרצ'ר נשארות בטוחות מבצעית עד לטמפרטורה של 4000 מעלות קלווין.",portal_ft)
        comparison_string = normalize("דע תיעצבמ תוחוטב תוראשנ ר'צרפא תויגולונכט לכ <cr>.ןיוולק תולעמ 4000 לש הרוטרפמטל <cr>")
        self.assertEqual(comparison_string, test_string)


    # def test_reddoor(self):
    #     test_string = "אני עדיין מרגיש שיש בינינו קצר בתקשורת. סטנלי עבר בדלת <clr:255,0,0>האדומה<clr:255,255,255>."
    #     comparison_string = normalize("רצק וניניב שיש שיגרמ ןיידע ינא <cr>תלדב רבע ילנטס .תרושקתב <cr><clr:255,0,0>המודאה<clr:255,255,255>. <cr>")
    #     self.assertEqual(comparison_string,normalize(rearrange_multiple_lines(test_string,ft.max_chars_before_break,None)))

if __name__ == '__main__':
    unittest.main()
