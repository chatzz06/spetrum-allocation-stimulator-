# ============================================================
# SpectrumSim - Best Fit Allocation Algorithm
# File: algorithms/best_fit.py
# ============================================================


def best_fit(available_bands, required_bandwidth):
    """
    Best Fit Spectrum Allocation Algorithm.

    Selects the smallest available frequency band
    that can accommodate the required bandwidth.

    Parameters:
        available_bands:
            List of tuples containing:
            (start_frequency, end_frequency)

        required_bandwidth:
            Required bandwidth in MHz.

    Returns:
        Allocated frequency range as:
            (start_frequency, end_frequency)

        Returns None if no suitable band exists.
    """

    # Validate bandwidth

    if required_bandwidth <= 0:
        return None


    best_band = None
    smallest_available = float("inf")


    # Search for the smallest suitable band

    for band in available_bands:

        start_frequency = band[0]
        end_frequency = band[1]

        available_bandwidth = (
            end_frequency - start_frequency
        )


        # Check whether this band can accommodate
        # the requested bandwidth

        if available_bandwidth >= required_bandwidth:

            if available_bandwidth < smallest_available:

                smallest_available = (
                    available_bandwidth
                )

                best_band = band


    # No suitable band found

    if best_band is None:
        return None


    # Allocate from the beginning of
    # the selected band

    allocated_start = best_band[0]

    allocated_end = (
        allocated_start +
        required_bandwidth
    )


    return (
        allocated_start,
        allocated_end
    )


# ============================================================
# UPDATE AVAILABLE BANDS
# ============================================================

def update_bands(
    available_bands,
    allocated_range
):
    """
    Remove the allocated frequency range
    from the available spectrum.
    """

    if allocated_range is None:
        return available_bands


    allocated_start = allocated_range[0]
    allocated_end = allocated_range[1]

    new_bands = []


    for band in available_bands:

        band_start = band[0]
        band_end = band[1]


        # If there is no overlap,
        # keep the original band

        if (
            allocated_end <= band_start
            or
            allocated_start >= band_end
        ):

            new_bands.append(band)

            continue


        # Remaining spectrum before allocation

        if allocated_start > band_start:

            new_bands.append(
                (
                    band_start,
                    allocated_start
                )
            )


        # Remaining spectrum after allocation

        if allocated_end < band_end:

            new_bands.append(
                (
                    allocated_end,
                    band_end
                )
            )


    return new_bands


# ============================================================
# COMPLETE BEST FIT ALLOCATION
# ============================================================

def perform_best_fit(
    available_bands,
    required_bandwidth
):
    """
    Perform Best Fit allocation.

    Returns:
        Dictionary containing:

        success
        allocation
        remaining_bands
        message
    """

    allocated_range = best_fit(
        available_bands,
        required_bandwidth
    )


    # Allocation failed

    if allocated_range is None:

        return {
            "success": False,
            "allocation": None,
            "remaining_bands": available_bands,
            "message": "No suitable spectrum available."
        }


    # Update remaining spectrum

    remaining_bands = update_bands(
        available_bands,
        allocated_range
    )


    return {
        "success": True,
        "allocation": allocated_range,
        "remaining_bands": remaining_bands,
        "message": "Spectrum allocated successfully using Best Fit."
    }


# ============================================================
# FIND BEST BAND
# ============================================================

def find_best_band(
    available_bands,
    required_bandwidth
):
    """
    Return the best frequency band without
    actually allocating it.
    """

    if required_bandwidth <= 0:
        return None


    best_band = None
    smallest_available = float("inf")


    for band in available_bands:

        start_frequency = band[0]
        end_frequency = band[1]

        available_bandwidth = (
            end_frequency - start_frequency
        )


        if (
            available_bandwidth >= required_bandwidth
            and
            available_bandwidth < smallest_available
        ):

            smallest_available = (
                available_bandwidth
            )

            best_band = band


    return best_band


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    # Example available spectrum

    available_bands = [
        (700, 720),
        (730, 780),
        (800, 850),
        (870, 950)
    ]


    # Required bandwidth

    required_bandwidth = 40


    print("======================================")
    print("        SpectrumSim - Best Fit")
    print("======================================")


    print("\nAvailable Spectrum:")

    for band in available_bands:

        print(
            band[0],
            "-",
            band[1],
            "MHz",
            "(",
            band[1] - band[0],
            "MHz)"
        )


    print(
        "\nRequired Bandwidth:",
        required_bandwidth,
        "MHz"
    )


    # Find best band

    best_band = find_best_band(
        available_bands,
        required_bandwidth
    )


    print("\n--------------------------------------")


    if best_band:

        print(
            "Best Suitable Band:",
            best_band[0],
            "-",
            best_band[1],
            "MHz"
        )

        print(
            "Band Size:",
            best_band[1] - best_band[0],
            "MHz"
        )

    else:

        print(
            "No suitable band found."
        )


    # Perform allocation

    result = perform_best_fit(
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