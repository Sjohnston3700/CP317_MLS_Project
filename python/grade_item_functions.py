
def modify_grade_max(grade_item, new_max):
    '''
    Function to try and update grade max.
    Preconditions:
        grade_item (GradeItem) : GradeItem object to be updated.
        new_max (string) : New maximum grade for the grade_item.
    Postconditions:
        If successful, The GradeItem is updated through the API.
        Returns:
            Errors (list) : Any and all errors that may have occured.
    '''
     
    errors = []
    if new_max is None:
        errors.append({'msg':'Missing new grade item maximum'})
    else:
        try:
            new_max = float(new_max)
        except:
            errors.append({'msg':'Grade maximum must be a number'})
            return errors
                   
        if new_max <= grade_item.get_max():
            errors.append({'msg':'New grade maximum must be larger than current maximum'})
        
        else:
            try:
                grade_item.set_max( new_max )
                return new_max
            except Exception as e:
                errors.append({'msg':str(e)})
    return errors