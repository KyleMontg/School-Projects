import argparse
import random
import time
import sys
sys.setrecursionlimit(200000)

def checkInputs(inputType, arraySize, sortType):
    if(not inputType == 'r' and not inputType == 'c' and not inputType == 's'):
        return False
    if(not arraySize > 0):
        return False
    if(not sortType == 'm' and not sortType == 'i' and not sortType == 's' and not sortType == 'q'):
        return False 
    return True

def quickSort(arr, low, high):
    if low < high:
        pivot = partition(arr, low, high)
        quickSort(arr, low, pivot-1)
        quickSort(arr, pivot+1, high)
        
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low,high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1

def mergeSort(arr, low, high):
    if low < high:
        middle = (low + high)//2
        mergeSort(arr, low, middle)
        mergeSort(arr, middle+1, high)
        merge(arr, low, middle, high)

def merge(arr, low, middle, high):
    leftLength = middle - low + 1
    rightLength = high - middle
    leftArr = [0] * (leftLength)
    rightArr = [0] * (rightLength)
    for i in range(0, leftLength):
        leftArr[i] = arr[low + i]
    for j in range(0, rightLength):
        rightArr[j] = arr[middle + j + 1]
    i, j = 0, 0
    k = low
    while i < leftLength and j < rightLength:
        if leftArr[i] <= rightArr[j]:
            arr[k] = leftArr[i]
            i += 1
        else: 
            arr[k] = rightArr[j]
            j += 1
        k += 1
    while i < leftLength:
        arr[k] = leftArr[i]
        i += 1
        k += 1 
    while j < rightLength:
        arr[k] = rightArr[j]
        j += 1
        k += 1 

def insertionSort(arr):
    for i in range(1, len(arr)):
        curr = arr[i]
        j = i - 1 
        while j >= 0 and curr < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = curr
        
def selectionSort(arr):
    for i in range(len(arr)):
        min = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min]:
                min = j
                arr[i], arr[min] = arr[min], arr[i]

if __name__ == '__main__':
    inputType, arraySize, sortType = None, None, None
    parser = argparse.ArgumentParser() #Grabs arguments
    try:
        parser.add_argument('inputType', type=str, nargs='?', default='r')
        parser.add_argument('arraySize', type=int, nargs='?', default=10)
        parser.add_argument('sortType', type=str, nargs='?', default='q')
        args = parser.parse_args()
        inputType, arraySize, sortType = args.inputType.lower(), args.arraySize, args.sortType.lower()
        if not checkInputs(inputType, arraySize, sortType):
            raise Exception('Invalid Input') 
    except Exception as e:
        print('Invalid command line arguments. Using defaults. Running quick sort on a random array of length 10') 
    finally:
        inputArray = []
        if(inputType == 'r'):
            inputArray = [random.randint(0, 100) for _ in range(arraySize)]
        elif(inputType == 'c'):
            inputArray = [5] * arraySize
        else:
            inputArray = list(range(arraySize))

        totalTime = 0
        if(sortType == 'm'):
            for i in range(3):
                startTime = time.time()
                a = mergeSort(inputArray, 0, len(inputArray) - 1)
                endTime = time.time()
                totalTime += endTime - startTime
            totalTime /= 3
            
        elif(sortType == 'i'):
            for i in range(3):
                startTime = time.time()
                a = insertionSort(inputArray)
                endTime = time.time()
                totalTime += endTime - startTime
            totalTime /= 3
            
        elif(sortType == 's'):
            for i in range(3):
                startTime = time.time()
                a = selectionSort(inputArray)
                endTime = time.time()
                totalTime += endTime - startTime
            totalTime /= 3
            
        else:
            for i in range(3):
                startTime = time.time()
                a = quickSort(inputArray, 0, len(inputArray)-1)
                endTime = time.time()
                totalTime += endTime - startTime
            totalTime /= 3
        print("{:.3f}".format(totalTime) + " Seconds")
