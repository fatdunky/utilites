def str2bool(v):
    ret_val = False
    try:
        ret_val = str(v).lower() in ("yes", "true", "t", "1", "y")
    except Exception:
        ret_val = False
    return ret_val
