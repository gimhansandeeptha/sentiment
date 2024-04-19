from src.servicenow.comment_request import get_customer_comments

def extract_messages(response):
    ''' Return two dimentional array, fist dimention is the account name and the second dimention is liat of comments
        Both the dimentions can be empty.
    '''
    # case_comments=[]

    try:
        data = response.json()
    except ValueError:
        raise ValueError("The object cannot be parsed")

    cases = data['result']['cases']
    extracted_cases =[]
    for case in cases:
        case_id = case.get('number', None)
        account = case.get('account', None)
        sys_created_on = case.get('sys_created_on', None)
        case_dict = {
            "case_id":case_id,
            "account": account,
            "sys_created_on": sys_created_on 
        }

        entries =[]
        for entry in case.get('entries',None):
            if entry is None or entry.get("element") != "comments":
                continue
            
            value = entry.get('value')
            created_on  = entry.get('sys_created_on')
            entry_dict = {
                "value" : value,
                "created_on" : created_on
            }
            entries.append(entry_dict)
        
        if entries:
            case_dict['entries'] = entries
            extracted_cases.append(case_dict)

    return extracted_cases


# query_params = {
#         "startDate": "2024-03-11",
#         "endDate": "2024-03-11"
#     }

# print(extract_messages(get_customer_comments(query_params)))
