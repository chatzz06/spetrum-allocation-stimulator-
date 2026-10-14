# ============================================================
# SpectrumSim - Interference Detection Algorithm
# File: algorithms/interference.py
# ============================================================


def check_overlap(start1, bandwidth1, start2, bandwidth2):
    """
    Check whether two frequency ranges overlap.

    Allocation 1:
        start1 -> start1 + bandwidth1

    Allocation 2:
        start2 -> start2 + bandwidth2
    """

    end1 = start1 + bandwidth1
    end2 = start2 + bandwidth2

    # No overlap
    if end1 <= start2 or end2 <= start1:
        return False

    return True


def calculate_overlap(start1, bandwidth1, start2, bandwidth2):
    """
    Calculate the amount of overlapping spectrum in MHz.
    """

    end1 = start1 + bandwidth1
    end2 = start2 + bandwidth2

    overlap_start = max(start1, start2)
    overlap_end = min(end1, end2)

    overlap = overlap_end - overlap_start

    if overlap <= 0:
        return 0

    return overlap


def calculate_interference_level(
    start1,
    bandwidth1,
    start2,
    bandwidth2
):
    """
    Calculate interference level based on
    the percentage of overlapping spectrum.
    """

    overlap = calculate_overlap(
        start1,
        bandwidth1,
        start2,
        bandwidth2
    )

    if overlap == 0:
        return 0

    smaller_bandwidth = min(
        bandwidth1,
        bandwidth2
    )

    if smaller_bandwidth <= 0:
        return 0

    percentage = (
        overlap / smaller_bandwidth
    ) * 100

    return round(percentage, 2)


def get_interference_status(level):
    """
    Convert interference percentage into a status.
    """

    if level == 0:
        return "No Interference"

    elif level <= 25:
        return "Low Interference"

    elif level <= 50:
        return "Medium Interference"

    else:
        return "High Interference"


def check_interference(
    start1,
    bandwidth1,
    start2,
    bandwidth2
):
    """
    Main interference checking function.

    Returns a dictionary containing:
        - overlap
        - interference level
        - status
    """

    overlap = calculate_overlap(
        start1,
        bandwidth1,
        start2,
        bandwidth2
    )

    level = calculate_interference_level(
        start1,
        bandwidth1,
        start2,
        bandwidth2
    )

    status = get_interference_status(level)

    return {
        "overlap": overlap,
        "interference_level": level,
        "status": status
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    # Allocation 1
    start1 = 700
    bandwidth1 = 50

    # Allocation 2
    start2 = 730
    bandwidth2 = 40

    result = check_interference(
        start1,
        bandwidth1,
        start2,
        bandwidth2
    )

    print("===================================")
    print("      SpectrumSim Interference")
    print("===================================")

    print(
        "Allocation 1:",
        start1,
        "-",
        start1 + bandwidth1,
        "MHz"
    )

    print(
        "Allocation 2:",
        start2,
        "-",
        start2 + bandwidth2,
        "MHz"
    )

    print(
        "Overlap:",
        result["overlap"], 
        "MHz"
    )

    print(
        "Interference:",
        result["interference_level"],
        "%"
    )

    print(
        "Status:",
        result["status"]
    )

    print("===================================")