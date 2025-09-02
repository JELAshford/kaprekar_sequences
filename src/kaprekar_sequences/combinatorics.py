import matplotlib.pyplot as plt
from math import comb
import numpy as np


def equivalence_classes(num_digits):
    return comb(num_digits + 9, 9)


def next_number_viz(number, num_digits):
    sorted_numbers = sorted(str(number).zfill(num_digits))
    min_num = int("".join(sorted_numbers))
    max_num = int("".join(sorted_numbers[::-1]))
    return max_num - min_num


def digit_signature(number, num_digits):
    return tuple(sorted(str(number).zfill(num_digits)))


def plot_equivalence_class_size(n_values=range(1, 50)):
    equiv_classes = [equivalence_classes(n) for n in n_values]
    total_nums = [10**n for n in n_values]
    reduction_factor = [
        total / equiv for total, equiv in zip(total_nums, equiv_classes)
    ]

    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    ax1.semilogy(n_values, total_nums, "b-o", label="Total numbers (10^N)", linewidth=2)
    ax1.semilogy(
        n_values,
        equiv_classes,
        "r-o",
        label="Equivalence classes C(N+9,9)",
        linewidth=2,
    )
    ax1.set_xlabel("Number of digits (N)")
    ax1.set_ylabel("Count (log scale)")
    ax1.set_title("Total Numbers vs Equivalence Classes")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.semilogy(n_values, reduction_factor, "g-o", linewidth=2, markersize=8)
    ax2.set_xlabel("Number of digits (N)")
    ax2.set_ylabel("Reduction factor (log scale)")
    ax2.set_title("Search Space Reduction Factor")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def distribution_of_classes_across_number_range(num_digits=6):
    # Analysis: Distribution of equivalence classes across number range
    total_range = 10**num_digits
    sample_sizes = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]

    print("Equivalence Class Coverage Analysis:")
    print(
        "Sample %    Numbers Checked    Unique Signatures    Total Possible    Coverage %"
    )
    print("-" * 75)

    total_possible = equivalence_classes(num_digits)

    for sample_pct in sample_sizes:
        sample_size = int(total_range * sample_pct)
        signatures = set()

        for i in range(sample_size):
            sig = digit_signature(i, num_digits)
            signatures.add(sig)

        coverage = len(signatures) / total_possible * 100
        print(
            f"{sample_pct * 100:6.1f}%    {sample_size:12,}    {len(signatures):15,}    {total_possible:12,}    {coverage:8.1f}%"
        )

    # Visualize distribution of equivalence classes across number range
    total_range_viz = 10**num_digits
    sample_every = 1  # Sample to keep reasonable size

    # Track when each equivalence class first appears
    first_appearance = {}
    equivalence_counts = {}
    positions = []
    equiv_indices = []

    for i in range(0, total_range_viz, sample_every):
        sig = digit_signature(i, num_digits)

        if sig not in first_appearance:
            first_appearance[sig] = i
            equivalence_counts[sig] = len(first_appearance)

        positions.append(i)
        equiv_indices.append(equivalence_counts[sig])

    # Create visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

    # Plot 1: Equivalence class index vs position in number sequence
    ax1.scatter(positions, equiv_indices, alpha=0.6, s=0.01)
    ax1.set_xlabel("Position in number sequence")
    ax1.set_ylabel("Equivalence class index (order of appearance)")
    ax1.set_title("Distribution of Equivalence Classes Across Number Range")
    ax1.grid(True, alpha=0.3)

    # Plot 2: Cumulative unique equivalence classes
    cumulative_unique = list(range(1, len(first_appearance) + 1))
    first_positions = sorted(first_appearance.values())
    ax2.plot(first_positions, cumulative_unique, "r-", linewidth=2)
    ax2.set_xlabel("Position in number sequence")
    ax2.set_ylabel("Cumulative unique equivalence classes discovered")
    ax2.set_title("Cumulative Discovery of Equivalence Classes")
    ax2.grid(True, alpha=0.3)

    # Add percentage markers
    for pct in [10, 25, 50, 75, 90]:
        pos = total_range_viz * pct / 100
        idx = np.searchsorted(first_positions, pos)
        if idx < len(cumulative_unique):
            coverage = cumulative_unique[idx] / len(first_appearance) * 100
            ax2.axvline(pos, color="gray", linestyle="--", alpha=0.7)
            ax2.text(
                pos,
                cumulative_unique[idx],
                f"{pct}% pos\n{coverage:.1f}% coverage",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=90,
            )

    plt.tight_layout()
    plt.show()

    print(f"Total equivalence classes found: {len(first_appearance)}")
    print(f"Expected total: {equivalence_classes(num_digits)}")
    print(f"Sample rate: every {sample_every} numbers")


def reachable_equivalence_classes(n_values=range(3, 17)):
    # Analysis: How reachable equivalence classes scale with digit count
    print("\nScaling Analysis: Reachable Equivalence Classes by Digit Count")

    first_step_reductions, second_step_reductions = [], []
    first_step_reachable_counts, second_step_reachable_counts = [], []

    for n in n_values:
        total_possible = equivalence_classes(n)
        first_step_reachable = set()
        second_step_reachable = set()

        # Sample every 1000th number to make it feasible for larger N
        sample_step = max(1, (10**n) // 10000000)

        for i in range(0, 10**n, sample_step):
            step1 = next_number_viz(i, n)
            sig1 = digit_signature(step1, n)
            first_step_reachable.add(sig1)

            step2 = next_number_viz(step1, n)
            sig2 = digit_signature(step2, n)
            second_step_reachable.add(sig2)

        first_step_reachable_count = len(first_step_reachable)
        first_step_reduction = total_possible / first_step_reachable_count
        first_step_reachable_counts.append(first_step_reachable_count)
        first_step_reductions.append(first_step_reduction)

        second_step_reachable_count = len(second_step_reachable)
        second_step_reduction = total_possible / second_step_reachable_count
        second_step_reachable_counts.append(second_step_reachable_count)
        second_step_reductions.append(second_step_reduction)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.plot(
        n_values,
        first_step_reductions,
        "b-o",
        label="After 1 Step",
        linewidth=2,
        markersize=8,
    )
    ax1.plot(
        n_values,
        second_step_reductions,
        "r-o",
        label="After 2 Steps",
        linewidth=2,
        markersize=8,
    )
    ax1.set_xlabel("Number of Digits (N)")
    ax1.set_ylabel("Reduction Factor")
    ax1.set_title("Reduction in Equivalence Classes")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(
        n_values,
        first_step_reachable_counts,
        "b-o",
        label="After 1 Step",
        linewidth=2,
        markersize=8,
    )
    ax2.plot(
        n_values,
        second_step_reachable_counts,
        "r-o",
        label="After 2 Steps",
        linewidth=2,
        markersize=8,
    )
    ax2.set_xlabel("Number of Digits (N)")
    ax2.set_ylabel("Reachable Equivalence Classes")
    ax2.set_title("Reachable Equivalence Classes")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def trajectory_analysis(num_digits=6, num_steps=3):
    """Analyze trajectories through transformation steps"""

    def track_trajectories(start_range, num_digits, num_steps=3, max_trajectories=1000):
        """Track how values evolve through transformation steps"""
        trajectories = []
        step_size = max(1, len(start_range) // max_trajectories)
        for start_val in start_range[::step_size]:
            trajectory = [start_val]
            current = start_val
            for step in range(num_steps):
                current = next_number_viz(current, num_digits)
                trajectory.append(current)
            trajectories.append(trajectory)
        return trajectories

    total_range_traj = 10**num_digits

    # Define different input ranges to compare
    ranges_to_analyze = {
        "First 10%": range(0, total_range_traj // 10),
        "Middle 10%": range(
            total_range_traj // 2 - total_range_traj // 20,
            total_range_traj // 2 + total_range_traj // 20,
        ),
        "Last 10%": range(total_range_traj * 9 // 10, total_range_traj),
        "Full Range (sample)": range(0, total_range_traj, total_range_traj // 1000),
    }

    # Create trajectory visualization
    fig, axes = plt.subplots(2, 2, figsize=(20, 15), sharey=True)
    axes = axes.flatten()
    colors = ["blue", "red", "green", "purple"]
    for ax, col, (_, input_range) in zip(axes, colors, ranges_to_analyze.items()):
        trajectories = track_trajectories(
            input_range, num_digits, num_steps, max_trajectories=500
        )
        for traj in trajectories:
            ax.plot(range(len(traj)), traj, alpha=0.3, color=col, linewidth=0.5)
    plt.tight_layout()
    plt.show()


# plot_equivalence_class_size()
# distribution_of_classes_across_number_range()
# reachable_equivalence_classes()
trajectory_analysis(num_digits=8, num_steps=5)
