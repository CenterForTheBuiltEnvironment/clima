

def psych_chart():
    if time_filters:
        if startMonth <= endMonth:
            mask = ((df['month'] < startMonth) | (df['month'] > endMonth))
            df[mask] = None
        else:
            mask = ((df['month'] >= endMonth) & (df['month'] <= startMonth))
            df[mask] = None

        if startHour <= endHour:
            mask = ((df['hour'] < startHour) | (df['hour'] > endHour))
            df[mask] = None
        else:
            mask = ((df['hour'] >= endHour) & (df['hour'] <= startHour))
            df[mask] = None

    if data_filters:
        if valMin <= valMax:
            mask = ((df[filter_variable] < valMin) |
                    (df[filter_variable] > valMax))
            df[mask] = None
        else:
            mask = ((df[filter_variable] >= valMax) &
                    (df[filter_variable] <= valMin))
            df[mask] = None

    var = ColorBy
    if var == "None":
        var_color = "darkorange"
    else:
        var_unit = str(var)+"_unit"
        var_unit = unit_dict[var_unit]

        var_name = str(var)+"_name"
        var_name = name_dict[var_name]

        var_color = str(var)+"_color"
        var_color = color_dict[var_color]

    if value_range == "global":
        # Set Global values for Max and minimum
        var_rangeX = DBT_range
        hr_range = [0, 0.03]
        var_rangeY = hr_range

    else:
        # Set maximumand minimum according to data
        dataMax = (5*math.ceil(df["DBT"].max()/5))
        dataMin = (5*math.floor(df["DBT"].min()/5))
        var_rangeX = [dataMin, dataMax]

        dataMax = (5*math.ceil(df["hr"].max()*1000/5))/1000
        dataMin = (5*math.floor(df["hr"].min()*1000/5))/1000
        var_rangeY = [dataMin, dataMax]

    Title = "Psychrometric Chart"

    if ColorBy != "None":
        Title = Title+" colored by "+var_name+" ("+var_unit+")"

    if apply_time_filters:
        Title = Title+"<br>between the months of " + \
            monthList[startMonth-1]+" and "+monthList[endMonth-1] + \
            " and between the hours " + \
            str(startHour)+":00 and "+str(endHour)+":00"
    if apply_data_filters:
        Title = Title+"<br>when the "+filter_variable + \
            " is between "+str(valMin)+" and "+str(valMax)+filter_unit

    dbt_list = list(range(-60, 60, 1))
    rh_list = list(range(10, 110, 10))

    rh_df = pd.DataFrame()
    for i, rh in enumerate(rh_list):
        hr_list = np.vectorize(psy.psy_ta_rh)(dbt_list, rh)
        hr_df = pd.DataFrame.from_records(hr_list)
        name = "rh"+str(rh)
        rh_df[name] = hr_df["hr"]

    fig = go.Figure()

    # Add traces
    for i, rh in enumerate(rh_list):
        name = "rh"+str(rh)
        fig.add_trace(go.Scatter(x=dbt_list, y=rh_df[name],
                                 showlegend=False,
                                 mode='lines',
                                 name="",
                                 hovertemplate="RH "+str(rh)+"%",
                                 line=dict(width=1,
                                           color="lightgrey"
                                           )))
    if var == "None":
        fig.add_trace(go.Scatter(x=df["DBT"], y=df["hr"],
                                 showlegend=False,
                                 mode='markers',
                                 marker=dict(size=6,
                                             color=var_color,
                                             showscale=False,
                                             opacity=0.2,
                                             ),
                                 hovertemplate=DBT_name+': %{x:.2f}'+DBT_unit,
                                 name=""
                                 ))

    else:
        fig.add_trace(go.Scatter(x=df["DBT"], y=df["hr"],
                                 showlegend=False,
                                 mode='markers',
                                 marker=dict(size=5,
                                             color=df[var],
                                             showscale=True,
                                             opacity=0.3,
                                             colorscale=var_color,
                                             colorbar=dict(
                                                 thickness=30,
                                                 title=var_unit+"<br>  ")
                                             ),
                                 customdata=np.stack(
                                     (df["RH"], df["h"], df[var], df["t_dp"]), axis=-1),
                                 hovertemplate=DBT_name+': %{x:.2f}'+DBT_unit +
                                 "<br>"+RH_name+': %{customdata[0]:.2f}'+RH_unit +
                                 "<br>"+h_name+': %{customdata[1]:.2f}'+h_unit +
                                 "<br>"+t_dp_name+': %{customdata[3]:.2f}'+t_dp_unit +
                                 "<br>" +
                                 "<br>"+var_name +
                                 ': %{customdata[2]:.2f}'+var_unit,
                                 name="",
                                 ))
    fig.update_xaxes(
        range=var_rangeX)
    fig.update_yaxes(
        range=var_rangeY)

    fig.update_layout(template=template, title=Title)
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='black', mirror=True)
    return fig
