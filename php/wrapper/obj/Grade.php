<?php 
    require_once 'API.php';
    require_once 'OrgMember.php';

class Grade
{
    protected $json;
    private $grade_item;
    private $student;

    /*
    Constructor:
    grade_item(GradeItem Object)
    student(OrgMember)
    comment (String)
    */
    function __construct($grade_item, $student, $comment) 
    {
        if (!is_subclass_of($this, 'Grade')) {
            throw new Exception('Grade must be subclassed');
        }
        $this->json = array(
        'UserId' => $student->get_id(),
        'OrgUnitId' => $student->get_org_id(),
        'Comments' => array(
        'Content' => $comment,
        'Type' => 'Text'
        ),
        'PrivateComments' => array(
        'Content' => '',
        'Type' => 'Text'
        )
        );
        $this->grade_item = $grade_item;
        $this->student = $student;
    }

    function get_json() 
    {
        return $this->json;
    }
    /*
    Return comments for this student with respect to this GradeItem
    */
    function get_comment()
    {
        return $this->json['Comments']['Content']; 
    }
    /*
    Return the GradeItem Object
    */
    function get_grade_item()
    {
        return $this->grade_item; 
         
        
    }
    
    /*
    Return the student object (OrgMember)
    */
    function get_student()
    {
        return $this->student;  
    }
    
    /*
    Call function to update grade
    */
    function put_grade()
    {
        put_grade(); 

    }
}
class NumericGrade extends Grade
{
    /*
    Constructor:
    grade_item(GradeItem Object)
       student(OrgMember)
       comment(feedbacks) string
       value(mark student scored) float
    */
    function __construct($grade_item, $student, $comment, $value) 
    {    

        if (is_nan($value)) {
            throw new Exception('Grade value must be numeric');
        }
        if ($value > $grade_item->get_max() && !$grade_item->can_exceed()) {
            throw new Exception('Grade value is greater than grade item max');
        }
        if ($value < 0) {
            throw new Exception('Grade value must be non-negative');
        }
        
        parent::__construct($grade_item, $student, $comment);
        $this->json['GradeObjectType'] = 1;
        $this->json['PointsNumerator'] = $value;
         
    }
    /*
    Returns value of the NumericGrade Item
    */
    function get_value() 
    {
        return $this->json['PointsNumerator'];
    }
    
}

?>
