import re


def _exapnd_regex(a, p, out_strings):
    one = False
    last = 0
    d = p.finditer(a)
    for e in d:
        one = True
        grp = e.group()
        if grp.startswith('(') and '){' in grp:
            grp = grp[1:]
            pattern, iter_name = grp.split('){')
        else:
            pattern, iter_name = grp.split('{')
        if iter_name.endswith('}'):
            iter_name = iter_name[:-1]
        min_iter, max_iter = iter_name.split(',')
        min_iter = int(min_iter)
        max_iter = int(max_iter)
        if min_iter == max_iter:
            pattern *= max_iter
            for i, s in enumerate(out_strings):
                out_strings[i] = s + a[last:e.start()] + pattern
        else:
            if min_iter > max_iter:
                raise Exception("Cannot expand regex: " + a)
            else:
                old_out_strings = out_strings[:]
                out_strings.clear()
                for z in range(min_iter, max_iter + 1):
                    for i in old_out_strings:
                        out_strings.append(i + a[last:e.start()] + pattern * z)
        last = e.end()
    return one, last


def expand_regex(a):
    out_strings = ['']
    b = re.compile('.\{[0-9]*,[0-9]*\}')
    c = re.compile('\(.*?\)\{[0-9]*,[0-9]*\}')
    one, last = _exapnd_regex(a, c, out_strings)
    if one:
        for i in range(len(out_strings)):
            out_strings[i] += a[last:]
    else:
        one, last = _exapnd_regex(a, b, out_strings)
        if one:
            for i in range(len(out_strings)):
                out_strings[i] += a[last:]
        else:
            yield a
            return
    for i in out_strings:
        yield from expand_regex(i)


class u_set(set):
    def __add__(self, other):
        return self.__class__(self.union(other))


class RegexElement(object):
    def __init__(self, string):
        self.string = string
        self.supersets = u_set()
        self.subsets = u_set()
        self.disjoints = u_set()
        self.intersects = u_set()
        self.maybes = []
        self.precompilation = {}
        self.compiled = re.compile(string, re.IGNORECASE)

    def __hash__(self):
        return hash(self.string)


SUPERSET = 'SUPERSET'
SUBSET = 'SUBSET'
INTERSECT = 'INTERSECT'
DISJOINT = 'DISJOINT'
EQUAL = 'EQUAL'

class SubsetGraph(object):
    def __init__(self, tests):
        self.regexps = []
        self.tests = tests
        self._dirty = True
        self._roots = None

    @property
    def roots(self):
        if self._dirty:
            r = self._roots = [i for i in self.regexps if not i.supersets]
            return r
        return self._roots

    def add_regex(self, new_regex):
        roots = self.roots
        new_re = RegexElement(new_regex)
        for element in roots:
            self.process(new_re, element)
        self.regexps.append(new_re)

    def process(self, new_re, element):
        relationship = self.compare(new_re, element)
        if relationship:
            getattr(self, 'add_' + relationship)(new_re, element)

    def add_SUPERSET(self, new_re, element):
        for i in element.subsets:
            i.supersets.add(new_re)
            new_re.subsets.add(i)

        element.supersets.add(new_re)
        new_re.subsets.add(element)

    def add_SUBSET(self, new_re, element):
        for i in element.subsets:
            self.process(new_re, i)

        element.subsets.add(new_re)
        new_re.supersets.add(element)

    def add_DISJOINT(self, new_re, element):
        for i in element.subsets:
            i.disjoints.add(new_re)
            new_re.disjoints.add(i)

        new_re.disjoints.add(element)
        element.disjoints.add(new_re)

    def add_INTERSECT(self, new_re, element):
        for i in element.subsets:
            self.process(new_re, i)

        new_re.intersects.add(element)
        element.intersects.add(new_re)

    def add_EQUAL(self, new_re, element):
        new_re.supersets = element.supersets.copy()
        new_re.subsets = element.subsets.copy()
        new_re.disjoints = element.disjoints.copy()
        new_re.intersects = element.intersects.copy()

    def compare(self, a, b):
        for test in self.tests:
            result = test(a.string, b.string)
            if result:
                return result

    def match(self, text, strict=True):
        matches = set()
        self._match(text, self.roots, matches)
        out = []
        for e in matches:
            for s in e.subsets:
                if s in matches:
                    break
            else:
                out.append(e)
        if strict and len(out) > 1:
            for i in out:
                print(i.string)
            raise Exception("Multiple equally specific matches found for " + text)
        return out

    def _match(self, text, elements, matches):
        new_elements = []
        for element in elements:
            m = element.compiled.match(text)
            if m:
                matches.add(element)
                new_elements.extend(element.subsets)
        if new_elements:
            self._match(text, new_elements, matches)


def check_equal(a, b):
    if a == b:
        return EQUAL

def check_prefixes(a, b):
    for i in range(len(a)):
        if i == len(b):
            break
        if a[i] in "(.[" or b[i] in "(.[)":
            break
        if a[i] != b[i]:
            return DISJOINT


def check_suffixes(a, b):
    for i in range(len(a)):
        if i == len(b):
            break
        if a[-i - 1] in ").]*+}?":
            try:
                if a[-i - 2] == "\\":
                    continue
            except IndexError:
                pass
            break
        elif b[-i - 1] in ").]*+}?":
            try:
                if b[-i - 2] == "\\":
                    continue
            except IndexError:
                pass
            break
        elif a[-i - 1] != b[-i - 1]:
            return DISJOINT


def check_dotstar(a, b):
    astar = False
    bstar = False

    if a.endswith(".*"):
        a = a[:-2]
        astar = True
    elif a.endswith("(/.*)?"):
        a = a[:-6]
        astar = True

    if b.endswith(".*"):
        b = b[:-2]
        bstar = True
    elif b.endswith("(/.*)?"):
        b = b[:-6]
        bstar = True

    if astar and bstar:
        if a.startswith(b):
            return SUBSET
        elif b.startswith(a):
            return SUPERSET
    elif bstar and a.startswith(b):
        return SUBSET
    elif astar and b.startswith(a):
        return SUPERSET


def check_fixed(a, b):
    a_fixed = True
    b_fixed = True

    i = 0
    while i < len(a):
        if a[i] == "\\":
            i += 1
        if a[i] in r"([.*{?+":
            a_fixed = False
        i += 1

    i = 0
    while i < len(b):
        if b[i] == "\\":
            i += 1
        if b[i] in r"([.*{?+":
            b_fixed = False
        i += 1

    if a_fixed and not b_fixed:
        if re.match(b, a):
            return SUBSET
    elif b_fixed and not a_fixed:
        if re.match(a, b):
            return SUPERSET


def check_match(a, b):
    if re.compile(a).match(b.rstrip('$').lstrip('^')):
        return SUPERSET
    if re.compile(b).match(a.rstrip('$').lstrip('^')):
        return SUBSET

def check_expand(a, b):
    c = list(expand_regex(a))
    d = list(expand_regex(b))
    bina = False
    ainb = False
    allainb = True
    allbina = True
    for i in c:
        if i in d:
            ainb = True
        else:
            allainb = False
    for i in d:
        if i in c:
            bina = True
        else:
            allbina = False
    if allainb and allbina:
        return EQUAL
    if allainb and not allbina:
        return SUBSET
    if allbina and not allainb:
        return SUPERSET
    if ainb or bina:
        return INTERSECT

default_tests = [check_expand, check_prefixes, check_fixed, check_dotstar, check_suffixes, check_equal, check_match]

if __name__=='__main__':
    sg = SubsetGraph(default_tests)
    sg.add_regex('..:..:..:..:..:..')
    sg.add_regex('^00:11:22:..:..:..')
    sg.add_regex('..:..:..:33:44:55$')
    print([i.string for i in sg.match('00:11:22:33:44:55', False)])
    sg.add_regex('^00:11:22:33:44:55$')
    print([i.string for i in sg.match('00:11:22:33:44:55', True)])
