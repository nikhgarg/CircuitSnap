import cv2;
import numpy as np;

#components has [x, y, w, h, elemchar]
def extractElements(components):
    components = dedup(components);
    components = combineLR(components);
    components = combineNumbers(components);
    components = combineUnits(components);
    elements = createElements(components);
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
            if distance(left, right) < 20:
                addedOhms += [combineComponents(left, right, 'o')];
    print addedOhms
    addedOhms = dedup(addedOhms);
    #add leftovers to components as well
    return componCopy + addedOhms;

#return components with digits combined into numbers
def combineNumbers(components):
    numbers = []
    componCopy =[]
    #extract l,r components into own arrays
    for ar in components:
        if ord(ar[4]) in range(ord('0'), ord('9') + 1):
            ar[4] = ord(ar[4]) - ord('0');
            numbers += [ar];
        else:
            componCopy += [ar]
    print numbers
    #make 3 nested passes
    for i in [0, 1, 2]:
        newnumbers = []
        indicesToRemove = []
        for i in range(0, len(numbers) - 1):
            for ii in range(i+1, len(numbers)):
                if distance(numbers[i], numbers[ii]) < 20:
                    if numbers[i][0] < numbers[ii][0]:
                        left = numbers[i];
                        right = numbers[ii];
                    else:
                        left = numbers[ii];
                        right = numbers[i];
                    combined = combineComponents(left, right, 10*left[4] + right[4]);
                    newnumbers += [combined]
                    indicesToRemove += [i, ii];
        print newnumbers;
        for i in range(0, len(numbers)):
            if i not in indicesToRemove:
                newnumbers += [numbers[i]];
        numbers = newnumbers;

    print numbers;
    return componCopy + numbers;

#combines numeric values with closest unit sign, creates sign if not there
def combineUnits(components):
    units = ['o', 'v', 'a'];

#creates elements from components and numeric values + units
def createElements(components):
    return []

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

def combineComponents(left, right, newvalue):
    return [left[0], int(round((left[1] + right[1])/2)), left[2] + right[2] + abs(left[0] - right[0]), max(left[3], right[3]), newvalue];