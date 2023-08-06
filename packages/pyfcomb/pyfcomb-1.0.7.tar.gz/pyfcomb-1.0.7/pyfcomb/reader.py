from pandas import DataFrame as df,concat
from typing import List, Tuple,Union
import numpy as np
import FCombLibrary as fc
import re

regex_string = r'([+-]*)(\d*)(f\d+)'

def _solution_strings(best_solution : str, other_solutions : List[str])->Tuple[str,Union[str,None]]:
    """
    'Beautifies' the solution strings.
    :param best_solution: String for the best solution
    :param other_solutions: Other solutions
    :return: Tuple containing beautified string as well as other solution
    """
    def get_str(solution : str) -> str:
        solution_str = f"{solution.split('=')[0]} = "
        #string shennanigans
        for sign,prefactor,f_id in re.findall(regex_string,solution.split('=')[1]):
            prefactor = prefactor if prefactor != "1" else ""
            multiplication_sign = '*' if prefactor != ""  else ''
            solution_str +=f" {sign} {prefactor}{multiplication_sign}{f_id}"
        return solution_str

    solutions_check_list = []
    best_solution_str = get_str(best_solution)

    split_list = re.split(r'[+-]', best_solution.split("=")[1])
    split_list.sort()
    solutions_check_list.append(split_list)

    if len(other_solutions) > 0:
        for other_solution in other_solutions:
            split_list = re.split(r'[+-]',other_solution.split("=")[1])
            split_list.sort()

            #check if any variant of solution is already added
            if split_list in solutions_check_list:
                continue

            try:
                other_solution_str += f',{get_str(other_solution)} '
            except UnboundLocalError:
                other_solution_str = f"{get_str(other_solution)} "
        try:
            return best_solution_str,other_solution_str
        except UnboundLocalError:
            return best_solution_str, None
    else:
        return best_solution_str,None

def _calculate_residual(solution : str, frequency : float, independent_frame : df) -> float:
    """
    Calculates residuals for a given solution.
    :param solution: solution string from FCombLibrary
    :param frequency: Frequency that the combination is computed for
    :param independent_frame: Frame containing the independent frequencies
    :return: Residual for the frequency and solution
    """
    equal_solution = solution.split("=")[1]
    val_list = []

    #calculate terms of solution
    for sign,prefactor,f_id in re.findall(regex_string,equal_solution):
        try:
            f = float(independent_frame[independent_frame.Name == f_id].Frequency)
        except:
            val_list.append(0)
            continue
        sign = -1 if sign == '-' else 1
        prefactor = int(prefactor)
        val_list.append(prefactor*sign*f)

    return abs(frequency - np.sum(val_list))

def _parse_frequencies(result: Tuple, frequency_ids: List[int], frequencies: List[float], amplitudes: List[float]) -> df:
    """
    Parses the list of frequencies from the result of FCombLibrary. The resulting frequencies are simply a list of
    combinations, where the first combination in this list is always the best combination
    :param result: FCombLibrary result
    :param frequency_ids: Unique Ids of the frequencies.
    :param frequencies: Responding frequencies
    :param amplitudes: Amplitudes of frequencies
    :return: Dataframe containing the combinations
    """
    combined_frequencies = result[0]
    unique_frequencies = result[1]
    f_ids = [f"f{i}" for i in frequency_ids]

    columns = ["Name","ID","Frequency","Amplitude","Solution","Residual","Independent","Other_Solutions"]

    independent_frame = []

    for f_id in unique_frequencies:
        idx = np.where(np.array(f_ids)==f_id)[0][0]
        independent_frame.append([f_id,frequency_ids[idx],frequencies[idx],amplitudes[idx],None,np.nan,True,None])

    independent_frame = df(independent_frame,columns=columns)

    combination_frame = []
    for solutions in combined_frequencies:
        solution_list = solutions.split(";")
        #best solution is always at first
        best_solution = solution_list[0]

        f_id = best_solution.split("=")[0]
        idx = np.where(np.array(f_ids)==f_id)[0][0]
        #calculate residual from best solution
        residual = _calculate_residual(best_solution,frequencies[idx],independent_frame)

        #remove best solution from the list
        solution_list.remove(best_solution)
        solution_list.remove(best_solution)

        best_solution,other_solution = _solution_strings(best_solution,np.unique(solution_list))

        combination_frame.append([f_id,frequency_ids[idx],frequencies[idx],amplitudes[idx],best_solution,residual,False,other_solution])

    combination_frame = df(combination_frame,columns=columns)
    return concat([independent_frame,combination_frame]).sort_values(['ID']).reset_index(drop=True)


def get_combinations(frequency_ids: List[int], frequencies: List[float], amplitudes: List[float], combo_depth: int = 4,
                     accuracy: float = 0.005):
    """
    Computes combinations of frequencies. Uses the FCombLibrary as a basis, and uses the returned strings to compute
    combinations. Returns a Dataframe, containing the frequencies, best solution (in this case the most accurate
    and least complex solution), residuals from this combination, as well as any other combination that is possible.
    :param frequency_ids: Unique Ids of the frequencies.
    :param frequencies: Responding frequencies
    :param amplitudes: Amplitudes of frequencies
    :param combo_depth: Depth of combination, by default 4
    :param accuracy: Minimum accuracy of the combination code
    :return: Dataframe containing the combined frequencies
    """
    if len(frequency_ids) != len(frequencies) or len(frequencies) != len(amplitudes):
        raise ValueError("Number of frequencies, amplitudes and frequency ids must be equal")

    data = [fc.FData(int(f_id), float(f), float(amp)) for f_id, f, amp in zip(frequency_ids, frequencies, amplitudes)]

    result = fc.get_combinations(data, combo_depth, accuracy)
    return _parse_frequencies(result,frequency_ids,frequencies,amplitudes)
