import cv2;
import numpy as np;

#components has [x, y, w, h, elemchar]

#return format:
#[x, y, w, h, ciruitelement, value_if_has_one]
    #possible elements: mesh, window, circuit, voltagesource, resistor, currentsource
    #                   m,      w,      c,      v,              r,          i
def extractElements(components):
    components = dedup(components);
    components = combineLR(components);
    [numbers, rest] = combineNumbers(components);
    [elements, remaining] = combineUnits(numbers, rest);

    # separate into units, numbers, and the rest
    #for the 'rest', combine into m, w, c, v, r, and i
        #combine +-S into v, S into i

    #to 'create elements', I need to connect a number to the correct unit to the correct source/resistor
        # if one of them is missing (either unit or source), then 1 is enough, need to fake a location
        # if value is missing, then need to figure something out...

    elements = createElements(elements, remaining);
    return elements;

#remove duplicate elements (same element in same place)
def dedup(components):
    return components

#return components but with lr combined into o
def combineLR(components):
    rights = []
    lefts = []
    componCopy =[]
    #extract l,r components into own arrays
    for ar in components:
        if ar[4] == 'r':
            rights += [ar]
        elif ar[4] == 'l':
            lefts += [ar]
        else:
            componCopy += [ar]

    #find closest matches
    print rights
    print lefts
    addedOhms = []
    #add matches to components
    for left in lefts:
        for right in rights:
            if distance(left, right) < 40:
                addedOhms += [combineComponents(left, right, 'o')];
    print addedOhms
    addedOhms = dedup(addedOhms);
    #add leftovers to components as well
    return componCopy + addedOhms;

#return components with digits combined into numbers
def combineNumbers(components):
    numbers = []
    componCopy =[]
    prefixes = {'k' : 1000, 'n' : .001};
    preelements = [];
    #extract l,r components into own arrays
    for ar in components:
        if ord(ar[4]) in range(ord('0'), ord('9') + 1):
            ar[4] = ord(ar[4]) - ord('0');
            numbers += [ar];
        elif ar[4] in prefixes.keys():
            preelements += [ar]
        else:
            componCopy += [ar]
    print numbers
    #make 3 nested passes
    for i in [0, 1, 2]:
        newnumbers = []
        indicesToRemove = []
        for i in range(0, len(numbers) - 1):
            if i in indicesToRemove:
                continue;
            minDistance = 1000000;
            ii = -1;
            for ifindmin in range(i+1,len(numbers)): 
                dist = distance(numbers[i], numbers[ifindmin]);
                if dist < minDistance and dist < 20 and (ifindmin not in indicesToRemove) :
                    ii = ifindmin;
                    minDistance = dist;
            if ii == -1:
                continue;
            if numbers[i][0] < numbers[ii][0]:
                left = numbers[i];
                right = numbers[ii];
            else:
                left = numbers[ii];
                right = numbers[i];
            combined = combineComponents(left, right, left[4]*pow(10, len(str(right[4]))) + right[4]);
            newnumbers += [combined]
            indicesToRemove += [i, ii];
        print newnumbers;
        for i in range(0, len(numbers)):
            if i not in indicesToRemove:
                newnumbers += [numbers[i]];
        numbers = newnumbers;
    print numbers
    newnumbers = [];
    indicesToRemove = []
    for i in range(0, len(numbers)):
        for ii in range(0, len(preelements)):
            if distance(numbers[i], preelements[ii]) < 20:
                combined = combineComponents(numbers[i], preelements[ii], numbers[i][4] * prefixes[preelements[ii][4]]);
                newnumbers += [combined];
                indicesToRemove += [i];
    for i in range(0, len(numbers)):
        if i not in indicesToRemove:
            newnumbers += [numbers[i]];
    numbers = newnumbers
    print numbers;
    return [numbers, componCopy]

#combines numeric values with closest unit sign, creates sign if not there
def combineUnits(numbers, others):
    elements = []
    units = ['o', 'v', 'a'];
    rest = []
    unit_components = [];

    for ar in others:
        if ar[4] in units:
            unit_components += [ar];
        else:
            rest += [ar]
    indicesToRemove = []
    print unit_components
    for i in range(0, len(numbers)):
        ii = -1;
        minDistance = 1000000;
        for ifindmin in range(0,len(unit_components)): 
            dist = distance(numbers[i], unit_components[ifindmin]);
            if dist < minDistance and dist < 40 and (ifindmin not in indicesToRemove) :
                ii = ifindmin;
                minDistance = dist;
        if ii == -1:
            continue;
        combined = combineComponents(numbers[i], unit_components[ii], unit_components[ii][4]);
        elements += [combined + [numbers[i][4]]];
        indicesToRemove += [ii];
    print elements;
    print rest;
    return [elements, rest];

#creates elements from components and numeric values + units
def createElements(elements, remaining):
    #TODO identify resistors before doing this
    #for now, connect v and a's to nearest sources, remove all other elements (+, -, spaces)
    #keep w, m, c for now
    #for now, assume right number of v's, s's, and a's (v + a = s)
    connection = {'o' : 'r', 'a' : 's', 'v' : 's'}; #a and v connect to s, o connects to r
    indicesToRemove = []
    for i in range(0, len(elements)):
        ii = -1;
        minDistance = 1000000;
        for ifindmin in range(0,len(remaining)): 
            dist = distance(elements[i][0:5], remaining[ifindmin]);
            if not connection[elements[i][4]] == remaining[ifindmin][4]:
                continue;
            if dist < minDistance and (ifindmin not in indicesToRemove):
                ii = ifindmin;
                minDistance = dist;
        if ii == -1:
            continue;
        elements[i][0] = remaining[ii][0]; #take on location of the element in the circuit
        elements[i][1] = remaining[ii][1];
        elements[i][2] = remaining[ii][2];
        elements[i][3] = remaining[ii][3];
        indicesToRemove += [ii];
    for i in remaining:
        if i[4] in ['w', 'm', 'c']:
            elements += [i];

    return elements

#returns 'distance' of 2 contours' -- probably do distance of center point
def distance(element1, element2):
    #x, y, w, h
    [x1, y1, w1, h1, cha1] = element1;
    [x2, y2, w2, h2, cha2] = element2;
    locCenter1 = [x1 + w1/2, y1 + h1/2];
    locCenter2 = [x2 + w2/2, y2 + h2/2];
    a = np.array(locCenter1, np.float32);
    b = np.array(locCenter2, np.float32);
    return np.linalg.norm(a-b)

#returns 'distance' of 2 contours' -- probably do distance of center point
def distance_resistor(elem, resistor):
    #x, y, w, h
    [x1, y1, w1, h1, cha1] = elem;
    [x2, y2, w2, h2, cha2] = resistor;

    #compare centers, top left to center, top right to center
    locCenter1 = [x1 + w1/2, y1 + h1/2];
    locCenter2 = [x2 + w2/2, y2 + h2/2];
    a = np.array(locCenter1, np.float32);
    b = np.array(locCenter2, np.float32);
    dist1 = np.linalg.norm(a-b);

    locCenter1 = [x1, y1];
    locCenter2 = [x2 + w2/2, y2 + h2/2];
    a = np.array(locCenter1, np.float32);
    b = np.array(locCenter2, np.float32);
    dist2 = np.linalg.norm(a-b);

    locCenter1 = [x1 + w1, y1 + h1/2];
    locCenter2 = [x2 + w2/2, y2 + h2/2];
    a = np.array(locCenter1, np.float32);
    b = np.array(locCenter2, np.float32);
    dist3 = np.linalg.norm(a-b);
    return min(dist1, dist2, dist3);

def combineComponents(left, right, newvalue):
    return [left[0], int(round((left[1] + right[1])/2)), left[2] + right[2] + abs(left[0] - right[0]), max(left[3], right[3]), newvalue];