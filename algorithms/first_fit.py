# ============================================================
# SpectrumSim - First Fit Allocation Algorithm
# File: algorithms/first_fit.py
# ============================================================


def first_fit(available_bands, required_bandwidth):
    """
    First Fit Spectrum Allocation Algorithm.

    Parameters:
        available_bands:
            List of available frequency bands.

            Example:
            [
                (700, 750),
                (750, 800),
                (800, 850)
            ]

        required_bandwidth:
            Required bandwidth in MHz.

    Returns:
        Allocated frequency range as a tuple:
            (start_frequency, end_frequency)

        If no suitable band is available:
            None
    """

    # Validate bandwidth

    if required_bandwidth <= 0:
        return None


    # Search bands from beginning to end

    for band in available_bands:

        start_frequency = band[0]
        end_frequency = band[1]

        available_bandwidth = (
            end_frequency - start_frequency
        )


        # First suitable band is selected

        if available_bandwidth >= required_bandwidth:

            allocated_start = start_frequency

            allocated_end = (
                start_frequency +
                required_bandwidth
            )

            return (
                allocated_start,
                allocated_end
            )


    # No suitable frequency band found

    return None


# ============================================================
# Allocate From Individual Frequency Range
# ============================================================

def allocate_frequency(
    start_frequency,
    end_frequency,
    required_bandwidth
):
    """
    Allocate bandwidth from a single frequency range.
    """

    available_bandwidth = (
        end_frequency - start_frequency
    )


    if required_bandwidth <= 0:
        return None


    if required_bandwidth > available_bandwidth:
        return None


    allocated_start = start_frequency

    allocated_end = (
        start_frequency +
        required_bandwidth
    )


    return (
        allocated_start,
        allocated_end
    )


# ============================================================
# Update Available Bands
# ============================================================

def update_bands(
    available_bands,
    allocated_range
):
    """
    Remove the allocated portion from
    the available frequency bands.
    """

    if allocated_range is None:
        return available_bands


    allocated_start = allocated_range[0]
    allocated_end = allocated_range[1]

    new_bands = []


    for band in available_bands:

        band_start = band[0]
        band_end = band[1]


        # No overlap

        if (
            allocated_end <= band_start
            or
            allocated_start >= band_end
        ):

            new_bands.append(band)

            continue


        # Remaining part before allocation

        if allocated_start > band_start:

            new_bands.append(
                (
                    band_start,
                    allocated_start
                )
            )


        # Remaining part after allocation

        if allocated_end < band_end:

            new_bands.append(
                (
                    allocated_end,
                    band_end
                )
            )


    return new_bands


# ============================================================
# Complete First Fit Allocation
# ============================================================

def perform_first_fit(
    available_bands,
    required_bandwidth
):
    """
    Perform First Fit allocation and
    return both allocation and updated bands.
    """

    allocated_range = first_fit(
        available_bands,
        required_bandwidth
    )


    if allocated_range is None:

        return {
            "success": False,
            "allocation": None,
            "remaining_bands": available_bands,
            "message": "No suitable spectrum available."
        }


    remaining_bands = update_bands(
        available_bands,
        allocated_range
    )


    return {
        "success": True,
        "allocation": allocated_range,
        "remaining_bands": remaining_bands,
        "message": "Spectrum allocated successfully."
    }


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    # Available frequency bands

    available_bands = [
        (700, 750),
        (750, 800),
        (800, 850),
        (850, 900),
        (900, 950)
    ]


    # Required bandwidth

    required_bandwidth = 20


    print("======================================")
    print("       SpectrumSim - First Fit")
    print("======================================")


    print("\nAvailable Spectrum:")

    for band in available_bands:

        print(
            band[0],
            "-",
            band[1],
            "MHz"
        )


    print(
        "\nRequired Bandwidth:",
        required_bandwidth,
        "MHz"
    )


    # Perform allocation

    result = perform_first_fit(
        available_bands,
        required_bandwidth
    )


    print("\n--------------------------------------")


    if result["success"]:

        allocation = result["allocation"]

        print(
            "Allocated Frequency:",
            allocation[0],
            "-",
            allocation[1],
            "MHz"
        )


        print(
            "Allocated Bandwidth:",
            allocation[1] - allocation[0],
            "MHz"
        )


        print("\nRemaining Spectrum:")

        for band in result["remaining_bands"]:

            print(
                band[0],
                "-",
                band[1],
                "MHz"
            )


    else:

        print(
            "Allocation Failed"
        )

        print(
            result["message"]
        )


    print("======================================")