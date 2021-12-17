def filter_by_hs(df_to_filter, hs_code, hs_code_vals):
    """
    Creating filters for every industry

    Args:
        df_to_filter:
        hs_code: HS Code 2, 4, 6
        hs_code_vals:

    Returns:
        DataFrame.
    """
    df_filter = (df_to_filter[hs_code].isin(hs_code_vals))
    filtered_df = df_to_filter[df_filter]
    return filtered_df


def complete_dfs(input_df, hs_codes_dict):
    """

    Args:
        input_df:
        hs_codes_dict:

    Returns:

    """
    result_dict = dict()
    for hs_code, sources_codes_dict in hs_codes_dict.items():
        for source, hs_code_values in sources_codes_dict.items():
            filtered_df = filter_by_hs(input_df, hs_code, hs_code_values)
            result_dict[source] = filtered_df
    return result_dict