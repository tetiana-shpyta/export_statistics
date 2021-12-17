def df_dropping(df_to_clean, cols_to_save):
    """
    Editing column 'HS Code 4 slice' -
    reducing the number of digits to 4

    Args:
        df_to_clean (DataFrame):
        cols_to_save:

    Returns:
        DataFrame

    """
    hs_code_4_slice = 'HS Code 4 slice'
    df_to_clean[hs_code_4_slice] = df_to_clean['HS Code 4'].str[:4]
    cols_to_save.append(hs_code_4_slice)
    needed_cols_df = df_to_clean[cols_to_save]
    return needed_cols_df


def typify_col(df_to_typify, cols_types_dict):
    """
    Modify types of values in columns to int|float

    Args:
        df_to_typify:
        cols_types_dict (dict):
        {'Export': 'float',
        'HS Code 2': 'int',
        'HS Code 4': 'int'}

    Returns:
        None.
    """
    for col_name, corresp_type in cols_types_dict.items():
        df_to_typify[f'{col_name} {corresp_type}'] = (df_to_typify[col_name]
                                                      .astype(corresp_type))
        df_to_typify.drop(col_name, axis=1, inplace=True)
    return df_to_typify