from counterfactuals.descriptor import RandomSampleDescriptor

def test():
    rd = RandomSampleDescriptor()
    rd.load_all()
    rd.gen_response()
    rd.fit_ps()
