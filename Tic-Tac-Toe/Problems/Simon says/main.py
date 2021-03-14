def what_to_do(instructions):
    return_str = ''
    if instructions.endswith("Simon says"):
        return_str = 'I ' + instructions[:instructions.find("Simon says")]
    elif instructions.startswith("Simon says"):
        return_str = 'I ' + instructions[11:]
    else:
        return_str = "I won't do it!"
    return return_str
