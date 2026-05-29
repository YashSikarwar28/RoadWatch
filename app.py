# RoadWatch Professional UI

import streamlit as st
import geopandas as gpd
from classifier import classify_road
from router import get_tn_highways_contact, get_gcc_contact      
from tender_lookup_csv import get_tender_details
from complaint_manager import save_complaint

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="RoadWatch",
    page_icon="🛣️",
    layout="wide"
)


# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
    padding-bottom: 1rem;
}

h1 {
    color: #0f172a;
    font-weight: 700;
}

.hero-text {
    color: #64748b;
    margin-top: -10px;
    margin-bottom: 25px;
    font-size: 17px;
}

.stTextInput > div > div > input {
    border-radius: 12px;
    border: 1px solid #d1d5db;
    padding: 12px;
}

.stTextArea textarea {
    border-radius: 12px;
    border: 1px solid #d1d5db;
}

.stSelectbox > div > div {
    border-radius: 12px;
}

.info-card {
    background-color: white;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.04);
    margin-bottom: 22px;
}

.footer {
    text-align: center;
    margin-top: 40px;
    color: #64748b;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# LOAD OSM DATA
# ---------------------------------------------------

@st.cache_data
def load_osm_data():

    gpkg_path = "data/osm/planet_80.11,12.783_80.612,13.099.gpkg"

    return gpd.read_file(
        gpkg_path,
        layer="lines"
    )


try:

    gdf = load_osm_data()

except Exception as e:

    st.error(f"Error loading OSM data: {e}")

    st.stop()


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("RoadWatch")

st.markdown("""
<div class="hero-text">
Smart Road Issue Routing & Authority Identification System
</div>
""", unsafe_allow_html=True)

st.divider()


# ---------------------------------------------------
# LAYOUT
# ---------------------------------------------------

left_col, right_col = st.columns([1, 2])


# ---------------------------------------------------
# LEFT PANEL
# ---------------------------------------------------

with left_col:

    st.markdown("### Submit Road Issue")
    st.caption("Provide details about the issue")

    road_name = st.text_input(
        "Road Name",
        placeholder="Example: Anna Salai"
    )

    issue_type = st.selectbox(
        "Issue Type",
        [
            "Pothole",
            "Road Damage",
            "Waterlogging",
            "Garbage",
            "Broken Streetlight",
            "Traffic Signal Issue"
        ]
    )

    description = st.text_area(
        "Issue Description",
        placeholder="Describe the issue briefly...",
        height=140
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">

        <h4>Note</h4>

        <p style="color:#64748b;">
        Please enter the correct road name for accurate results.
        </p>

    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------
# RIGHT PANEL
# ---------------------------------------------------

with right_col:

    st.subheader("Results")

    # ---------------------------------------------------
    # WAIT FOR INPUT
    # ---------------------------------------------------

    if road_name.strip() == "":

        st.info(
            "Enter a road name to begin."
        )

    else:

        # ---------------------------------------------------
        # FIND MATCHES
        # ---------------------------------------------------

        matches = gdf[
            gdf["name"].str.contains(
                road_name,
                case=False,
                na=False
            )
        ]

        if matches.empty:

            st.error(
                "Road not found in dataset."
            )

        else:

            # ---------------------------------------------------
            # KEEP ONLY VALID ROADS
            # ---------------------------------------------------

            valid_matches = matches[
                matches["highway"].notna()
            ]

            valid_matches = valid_matches[
                valid_matches["name"].notna()
            ]

            # ---------------------------------------------------
            # CLEAN ROAD OPTIONS
            # ---------------------------------------------------

            road_options = sorted(
                valid_matches["name"]
                .astype(str)
                .unique()
            )

            if len(road_options) == 0:

                st.error(
                    "No valid road information found."
                )

                st.stop()

            # ---------------------------------------------------
            # ROAD SELECTION
            # ---------------------------------------------------

            selected_road = st.selectbox(
                "Select Matching Road",
                road_options
            )

            # ---------------------------------------------------
            # GET SELECTED ROAD
            # ---------------------------------------------------

            selected_matches = valid_matches[
                valid_matches["name"] == selected_road
            ]

            if selected_matches.empty:

                st.error(
                    "No usable road segment found."
                )

                st.stop()

            # Use first stable segment
            selected_match = (
                selected_matches
                .sort_index()
                .iloc[0]
            )

            road_name_found = selected_match["name"]

            highway_type = selected_match["highway"]

            # ---------------------------------------------------
            # CLASSIFICATION
            # ---------------------------------------------------

            road_class, authority = classify_road(
                highway_type
            )

            # ---------------------------------------------------
            # CONTACT DETAILS
            # ---------------------------------------------------

            if authority == "TN Highways":

                contacts = get_tn_highways_contact(
                    road_name_found
                )

                email = contacts["E-mail ID"]

                email = (
                    email
                    .replace("[at]", "@")
                    .replace("[dot]", ".")
                )

                contact_person = contacts[
                    "Contact Person"
                ]

                district = contacts["District"]

                phone = contacts["Phone No."]

            else:

                contacts = get_gcc_contact()

                contact_person = contacts[
                    "Contact Person"
                ]

                district = contacts["District"]

                phone = contacts["Phone No."]

                email = contacts["E-mail ID"]

            # ---------------------------------------------------
            # ROAD INFORMATION
            # ---------------------------------------------------

            with st.container(border=True):

                st.markdown(
                    "### Road Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Road Found",
                        road_name_found
                    )

                    st.metric(
                        "Road Type",
                        highway_type
                    )

                with col2:

                    st.metric(
                        "Road Class",
                        road_class
                    )

                    st.metric(
                        "Authority",
                        authority
                    )

            st.markdown("<br>",
                        unsafe_allow_html=True)



            # ---------------------------------------------------
            # TENDER INFORMATION
            # ---------------------------------------------------

            tender = get_tender_details(
                road_name_found
            )

            if tender:

                with st.container(border=True):

                    st.markdown(
                        "### Recent Government Work"
                    )

                    st.write(
                        "**Work:**",
                        tender["work"]
                    )

                    st.write(
                        "**Department:**",
                        tender["department"]
                    )

                    st.write(
                        "**Budget:**",
                        tender["budget"]
                    )

                    st.write(
                        "**Date:**",
                        tender["date"]
                    )

            else:

                with st.container(border=True):

                    st.markdown(
                        "### Recent Government Work"
                    )

                    st.info(
                        "No tender information available."
                    )

            st.markdown(
                "<br>",
                unsafe_allow_html=True
            )


            # ---------------------------------------------------
            # CONTACT INFO
            # ---------------------------------------------------

            with st.container(border=True):

                st.markdown(
                    "### Authority Contact"
                )

                st.write(
                    "**Contact Person:**",
                    contact_person
                )

                st.write(
                    "**District:**",
                    district
                )

                st.write(
                    "**Phone:**",
                    phone
                )

                st.write(
                    "**Email:**",
                    email
                )

            st.markdown("<br>",
                        unsafe_allow_html=True)
            

            # ---------------------------------------------------
            # COMPLAINT SUMMARY
            # ---------------------------------------------------

            with st.container(border=True):

                st.markdown(
                    "### Complaint Summary"
                )

                st.write(
                    "**Issue Type:**",
                    issue_type
                )

                st.write(
                    "**Description:**",
                    description
                )

                st.markdown("---")

                if st.button(
                    "Submit Complaint"
                ):

                    complaint_id = (
                        save_complaint(
                            road_name_found,
                            issue_type,
                            description
                        )
                    )

                    st.success(
                        f"Complaint Submitted Successfully! "
                        f"Complaint ID: {complaint_id}"
                    )


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("""
<div class="footer">
RoadWatch MVP • Civic Technology Initiative
</div>
""", unsafe_allow_html=True)

