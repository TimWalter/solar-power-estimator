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
