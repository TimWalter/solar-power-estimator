from dataclasses import dataclass, field


@dataclass
class ID:
    @dataclass
    class Input:
        @dataclass
        class Location:
            name: str = "location_name"
            map: str = "location_map"
            latitude: str = "location_latitude"
            longitude: str = "location_longitude"
            altitude: str = "location_altitude"

        location: Location = field(default_factory=Location)
        time: str = "time"

        @dataclass
        class PV:
            @dataclass
            class Panel:
                manufacturer: str = "pv_panel_manufacturer"
                series: str = "pv_panel_series"
                model: str = "pv_panel_model"

                @dataclass
                class Custom:
                    button: str = "pv_panel_custom_button"
                    save: str = "pv_panel_save_custom_button"
                    fade: str = "pv_panel_custom_fade"
                    success: str = "pv_panel_custom_success"
                    manufacturer_store: str = "pv_panel_custom_manufacturer_store"
                    series_store: str = "pv_panel_custom_series_store"
                    model_store: str = "pv_panel_custom_model_store"

                custom: Custom = field(default_factory=Custom)

                @dataclass
                class Stats:
                    accordion: str = "pv_panel_panel_stats_accordion"
                    v_mp: str = "pv_panel_panel_stats_v_mp"
                    i_mp: str = "pv_panel_panel_stats_i_mp"
                    v_oc: str = "pv_panel_panel_stats_v_oc"
                    i_sc: str = "pv_panel_panel_stats_i_sc"
                    t_v_oc: str = "pv_panel_panel_stats_t_v_oc"
                    t_i_sc: str = "pv_panel_panel_stats_t_i_sc"
                    t_p_mp: str = "pv_panel_panel_stats_t_p_mp"
                    technology: str = "pv_panel_panel_stats_technology"
                    n_cells_series: str = "pv_panel_panel_stats_n_cells_series"

                stats: Stats = field(default_factory=Stats)

            panel: Panel = field(default_factory=Panel)
            case: str = "pv_case"
            number_of_modules: str = "pv_number_of_modules"

            @dataclass
            class Tilt:
                radio: str = "pv_tilt_opt"

                @dataclass
                class Fix:
                    collapse: str = "pv_tilt_fix_collapse"
                    input: str = "pv_tilt_fix_input"
                    column: str = "pv_tilt_fix_column"

                fix: Fix = field(default_factory=Fix)

                @dataclass
                class Constrain:
                    collapse: str = "pv_tilt_constrain_collapse"
                    min: str = "pv_tilt_constrain_min"
                    max: str = "pv_tilt_constrain_max"
                    column: str = "pv_tilt_constrain_column"

                constrain: Constrain = field(default_factory=Constrain)

            tilt: Tilt = field(default_factory=Tilt)

            @dataclass
            class Azimuth:
                radio: str = "pv_azimuth_opt"

                @dataclass
                class Fix:
                    collapse: str = "pv_azimuth_fix_collapse"
                    input: str = "pv_azimuth_fix_input"

                fix: Fix = field(default_factory=Fix)

                @dataclass
                class Constrain:
                    collapse: str = "pv_azimuth_constrain_collapse"
                    min: str = "pv_azimuth_constrain_min"
                    max: str = "pv_azimuth_constrain_max"

                constrain: Constrain = field(default_factory=Constrain)

            azimuth: Azimuth = field(default_factory=Azimuth)

            @dataclass
            class Bipartite:
                button: str = "pv_bipartite_button"
                collapse: str = "pv_bipartite_collapse"
                side1: str = "pv_bipartite_side1"
                side2: str = "pv_bipartite_side2"

            bipartite: Bipartite = field(default_factory=Bipartite)

            @dataclass
            class Inverter:
                manufacturer: str = "pv_inverter_manufacturer"
                series: str = "pv_inverter_series"
                model: str = "pv_inverter_model"

                @dataclass
                class Custom:
                    button: str = "pv_inverter_custom_button"
                    save: str = "pv_inverter_save_custom_button"
                    fade: str = "pv_inverter_custom_fade"
                    success: str = "pv_inverter_custom_success"
                    manufacturer_store: str = "pv_inverter_custom_manufacturer_store"
                    series_store: str = "pv_inverter_custom_series_store"
                    model_store: str = "pv_inverter_custom_model_store"

                custom: Custom = field(default_factory=Custom)

                @dataclass
                class Stats:
                    accordion: str = "pv_inverter_inverter_stats_accordion"
                    paco: str = "pv_inverter_inverter_stats_paco"
                    pdco: str = "pv_inverter_inverter_stats_pdco"
                    vdco: str = "pv_inverter_inverter_stats_vdco"
                    pso: str = "pv_inverter_inverter_stats_pso"
                    c0: str = "pv_inverter_inverter_stats_c0"
                    c1: str = "pv_inverter_inverter_stats_c1"
                    c2: str = "pv_inverter_inverter_stats_c2"
                    c3: str = "pv_inverter_inverter_stats_c3"
                    pnt: str = "pv_inverter_inverter_stats_pnt"

                stats: Stats = field(default_factory=Stats)

            inverter: Inverter = field(default_factory=Inverter)

        pv: PV = field(default_factory=PV)

    input: Input = field(default_factory=Input)

    @dataclass
    class Control:
        start: str = "control_start"

        @dataclass
        class Cancel:
            fade: str = "control_cancel_fade"
            button: str = "control_cancel_button"

        cancel: Cancel = field(default_factory=Cancel)

        @dataclass
        class Loading:
            gif: str = "control_loading_gif"
            placeholder: str = "control_loading_placeholder"

        loading: Loading = field(default_factory=Loading)
        progress_bar: str = "control_progress_bar"

    control: Control = field(default_factory=Control)

    @dataclass
    class Output:
        table: str = "output_table"
        graph: str = "output_graph"

    output: Output = field(default_factory=Output)


ids = ID()
