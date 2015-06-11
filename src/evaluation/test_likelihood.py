import sys,os


"""
compute the held-out likelihood by blei's lda implementation.

dependency:
blei's lda-c-dist installed under $ROOT/tool/blei

input:
1. model beta file
    .beta contains the log of the topic distributions.
    Each line is a topic; in line k, each entry is log p(w | z=k)
2. model alpha file
    .other contains alpha.

    For example:
    num_topics 20
    num_terms 21774
    alpha 0.015
3. held-out text file

output:
likelihood

"""


def run_lda_inference(lda, settings, model, data):
    """
    Refer to blei's lda readme
    run "lda inf [settings] [model] [data] [name]"
    """
    name = '.run_lda'
    command = lda + ' inf ' + settings + ' ' + model + ' ' + data + ' ' + name

    ret = os.system(command)
    if ret:
        # something wrong
        return 0, ret

    #calc the likelihood
    l_file = name + '-lda-lhood.dat'
    num_docs =0
    l_sum =0
    with open(l_file, 'r') as file:
        for line in file:
            num_docs+=1
            l_sum+= float(line.rstrip())

    return num_docs, l_sum/float(num_docs)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: test_likelihood <lda-install-path> <model-name> <data>')
        sys.exit(0)

    # check the path
    ldaPath = sys.argv[1]
    modelname = sys.argv[2]
    data = sys.argv[3]

    lda = ldaPath + '/lda'
    settings = ldaPath + '/inf-settings.txt'
    local_settings = '.inf-settings.txt'
    beta = modelname + '.beta'
    other = modelname + '.other'
    
    if os.path.exists(lda) and os.path.exists(settings):
        if os.path.exists(beta) and os.path.exists(other):
            if os.path.exists(data):
                if os.path.exists(local_settings):
                    doccnt, likelihood = run_lda_inference(lda, local_settings, modelname, data)
                else:
                    doccnt, likelihood = run_lda_inference(lda, settings, modelname, data)
                if doccnt:
                    print('doccnt = %d, likelihood = %f\n'%(doccnt, likelihood))
                else:
                    print('Error: run command failed\n')
            else:
                print('Error: data file not exists!\n')
        else:
            print('Error: .beta or .other file not found at %s, %s\n'%(beta, other))
    else:
        print('Error: lda not found at %s\n'%lda)
    












