

from spn.io.Text import str_to_spn
def read_spn_from_equationFile(filename):
    f = open(filename, "r")
    spnStr = f.read()
    spn = str_to_spn(spnStr)
    return spn


from spn.io.Text import spn_to_str_equation

def write_spn_as_equationFile(spn, filename):
    spnStr = spn_to_str_equation(spn)
    f = open(filename, "w")
    f.write(spnStr)
    f.close()


from spn.io.Text import to_JSON

def write_spn_as_JSONFile(spn, filename):
    spnJSONStr = to_JSON(spn)
    f = open(filename, "w")
    f.write(spnJSONStr)
    f.close()


def read_spn_from_JSONFile(spn, filename):
    raise NotImplementedError

 #to_JSON(spn)