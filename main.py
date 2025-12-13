from datetime import datetime

from sympy import (
    And, Complement, Eq, Intersection, Interval, SymmetricDifference,
    solve, symbols)
from sympy import Union as sympy_Union


def print_intervals(
        interval_or_intervals: Interval | sympy_Union,
        interval_name: str
) -> True:
    if isinstance(interval_or_intervals, Interval):
        print(f"\n{interval_name}:\n"
              f"\t{datetime.fromtimestamp(float(interval_or_intervals.start))} - "
              f"{datetime.fromtimestamp(float(interval_or_intervals.end))}")
    elif isinstance(interval_or_intervals, (sympy_Union, Intersection)):
        print(f"\n{interval_name}:\n"
              f"\tlen(interval_or_intervals.args): {len(interval_or_intervals.args)}\n"
              f"\tinterval_or_intervals.args: {interval_or_intervals.args}")
        for cur_united_interval in interval_or_intervals.args:
            print("\t\tsub-interval: "
                  f"{datetime.fromtimestamp(float(cur_united_interval.start))} - "
                  f"{datetime.fromtimestamp(float(cur_united_interval.end))}")
    else:
        print(f"\n{interval_name}:\n"
              f"\ttype(interval_or_intervals): {type(interval_or_intervals)}"
              f"interval_or_intervals: {interval_or_intervals}")


x, y, k = symbols("x y k")

equation_1 = Eq(x + y, (x * y) / k)
equation_2 = Eq(x - y, x + y ** 3)

solution = solve((equation_1, equation_2), (x, y, k))
print("solution:", solution)

start_time_12_00 = datetime(year=2025, month=1, day=1, hour=12, minute=00).timestamp()
start_time_12_35 = datetime(year=2025, month=1, day=1, hour=12, minute=35).timestamp()
end_time_12_45 = datetime(year=2025, month=1, day=1, hour=12, minute=45).timestamp()
end_time_13_00 = datetime(year=2025, month=1, day=1, hour=13, minute=00).timestamp()

check_time = datetime(year=2025, month=1, day=1, hour=13, minute=00).timestamp()
print("start_time_12_00:", start_time_12_00)
print("end_time_13_00:", end_time_13_00)
print("check_time:", check_time)

start, end, cur_time = symbols("start end cur_time")

interval_via_and = And(start_time_12_00 <= cur_time, cur_time < end_time_13_00)
print("\ninterval_via_and:", interval_via_and)

is_included_via_and = interval_via_and.subs(cur_time, check_time)
print("\tis_included_via_and:", is_included_via_and)

int_12_00_to_13_00 = Interval(start=start_time_12_00, end=end_time_13_00, right_open=False)
print("\nint_12_00_to_13_00:", int_12_00_to_13_00)

is_included_via_interval_opt_1 = int_12_00_to_13_00.contains(check_time)
print("\tis_included_via_interval_opt_1:", is_included_via_interval_opt_1)

is_included_via_interval_opt_2 = check_time in int_12_00_to_13_00
print("\tis_included_via_interval_opt_2:", is_included_via_interval_opt_2)

# Defining outer interval, inner interval and empty (zero-based) interval
outer_12_00_to_13_00 = Interval(start=start_time_12_00, end=end_time_13_00)
inner_12_35_to_12_45 = Interval(start=start_time_12_35, end=end_time_12_45)
empty_int_00_00_to_00_00 = Interval(start=0, end=0, left_open=True, right_open=True)

is_subset_interval = inner_12_35_to_12_45.is_subset(outer_12_00_to_13_00)
print("\tis_subset_interval:", is_subset_interval)

is_superset_interval = outer_12_00_to_13_00.is_superset(inner_12_35_to_12_45)
print("\tis_superset_interval:", is_superset_interval)

# Check interval is empty
is_empty_interval = empty_int_00_00_to_00_00.is_empty
print("\tis_empty_interval:", is_empty_interval)

# Summarise outer interval, inner interval and empty one
outer_inner_sum_opt_1 = outer_12_00_to_13_00 + inner_12_35_to_12_45 + empty_int_00_00_to_00_00
print_intervals(interval_or_intervals=outer_inner_sum_opt_1,
                interval_name="outer_inner_sum_opt_1")

outer_inner_sum_opt_2 = sympy_Union(outer_12_00_to_13_00, inner_12_35_to_12_45, empty_int_00_00_to_00_00)
print_intervals(interval_or_intervals=outer_inner_sum_opt_2,
                interval_name="outer_inner_sum_opt_2")

# Substitute outer intervals, inner interval and empty one
outer_inner_subt_opt_1 = outer_12_00_to_13_00 - inner_12_35_to_12_45 - empty_int_00_00_to_00_00
print_intervals(interval_or_intervals=outer_inner_subt_opt_1,
                interval_name="outer_inner_subt_opt_1")

outer_inner_subt_opt_2 = Complement(a=outer_12_00_to_13_00,
                                    b=inner_12_35_to_12_45)
print_intervals(interval_or_intervals=outer_inner_subt_opt_2,
                interval_name="outer_inner_subt_opt_2")

# Defining intervals with overlapping
start_overlap_12_00_to_12_45 = Interval(start=start_time_12_00, end=end_time_12_45)
end_overlap_12_35_to_13_00 = Interval(start=start_time_12_35, end=end_time_13_00)

# Summarise overlapped intervals and empty interval
start_end_overlap_sum_opt_1 = start_overlap_12_00_to_12_45 + end_overlap_12_35_to_13_00 + empty_int_00_00_to_00_00
print_intervals(interval_or_intervals=start_end_overlap_sum_opt_1,
                interval_name="start_end_overlap_sum_opt_1")


start_end_overlap_sum_opt_2 = sympy_Union(start_overlap_12_00_to_12_45, end_overlap_12_35_to_13_00)
print_intervals(interval_or_intervals=start_end_overlap_sum_opt_2,
                interval_name="start_end_overlap_sum_opt_2")

# Substitute overlapped intervals and empty interval
start_end_overlap_subt = start_overlap_12_00_to_12_45 - end_overlap_12_35_to_13_00 - empty_int_00_00_to_00_00
print_intervals(interval_or_intervals=start_end_overlap_subt,
                interval_name="start_end_overlap_subt")

end_start_overlap_subt = end_overlap_12_35_to_13_00 - start_overlap_12_00_to_12_45 - empty_int_00_00_to_00_00
print_intervals(interval_or_intervals=end_start_overlap_subt,
                interval_name="end_start_overlap_subt")

# Time intervals intersections
outer_inner_intersect_opt_1 = outer_12_00_to_13_00.intersect(inner_12_35_to_12_45)
print_intervals(interval_or_intervals=outer_inner_intersect_opt_1,
                interval_name="outer_inner_intersect_opt_1")


outer_inner_intersect_opt_2 = Intersection(
    outer_12_00_to_13_00, inner_12_35_to_12_45, empty_int_00_00_to_00_00)
print_intervals(interval_or_intervals=outer_inner_intersect_opt_2,
                interval_name="outer_inner_intersect_opt_2")

# Time intervals symmetric difference
outer_inner_symmetric_diff_opt_1 = (
        (outer_12_00_to_13_00 + inner_12_35_to_12_45 + empty_int_00_00_to_00_00) -
        Intersection(outer_12_00_to_13_00, inner_12_35_to_12_45, empty_int_00_00_to_00_00))
print_intervals(interval_or_intervals=outer_inner_symmetric_diff_opt_1,
                interval_name="outer_inner_symmetric_diff_opt_1")

outer_inner_symmetric_diff_opt_2 = SymmetricDifference(
    a=outer_12_00_to_13_00, b=inner_12_35_to_12_45)
print_intervals(interval_or_intervals=outer_inner_symmetric_diff_opt_2,
                interval_name="outer_inner_symmetric_diff_opt_2")
