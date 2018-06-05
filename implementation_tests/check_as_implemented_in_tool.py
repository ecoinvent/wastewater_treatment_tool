import json
import os
import pprint
import sys

#print python version before local imports
print("Running Python",sys.version.split(' ')[0])

#folder with python packages
sys.path.append(r"C:\mypy\code")
sys.path.append("wastewater_treatment_tool")
import xlrd

#from {folder}.{folder} import {file}
from pycode import DirectDischarge_ecoSpold, WWT_ecoSpold
from pycode.placeholders import *
from pycode.defaults import *

#go to tests folder
os.chdir(r'C:\mypy\code\wastewater_treatment_tool')
root_dir = os.getcwd()
#print("Root dir is",root_dir)

'''Receive a json string from stdin'''
from_tool = {
  "inputs": {
    "activity_name": "asdfasd",
    "geography": "GLO",
    "untreated_fraction": 0.2679174264,
    "tool_use_type": "specific",
    "PV": {
      "value": 365.25,
      "unit": "m3/year"
    },
    "CSO_particulate": {
      "value": 0.01,
      "unit": "ratio"
    },
    "CSO_soluble": {
      "value": 0.02,
      "unit": "ratio"
    },
    "fraction_C_fossil": {
      "value": 0.036000000000000004,
      "unit": "ratio"
    },
    "COD_TOC_ratio": {
      "value": 3,
      "unit": "g_COD/g_TOC"
    },
    "url": "http://prqv.vps.infomaniak.com/ecoinvent/n-wwtp.php?activity_name=asdfasd&geography=GLO&ww_type=municipal&wwtp_type=specific&Q=1&T=12&COD=300&TKN=35&TP=6&Ag=0&Al=1.0379&As=0.0009&B=0&Ba=0&Be=0&Br=0&Ca=50.834&Cd=0.0003&Cl=30.031&Co=0.0016&Cr=0.0122&Cu=0.0374&F=0.0328&Fe=7.0928&Hg=0.0002&I=0&K=0.3989&Mg=5.7071&Mn=0.053&Mo=0.001&Na=2.186&Ni=0.0066&Pb=0.0086&Sb=0&Sc=0&Se=0&Si=3.1263&Sn=0.0034&Sr=0&Ti=0&Tl=0&V=0&W=0&Zn=0.1094&",
    "technologies_averaged": [
      {
        "fraction": 1,
        "capacity": 50000,
        "class": "wastewater treatment facility, capacity class 2, between 50,000 and 100,000 PE",
        "location": "GLO",
        "technology_level_1": "aerobic intensive",
        "technology_level_2": "110000"
      }
    ],
    "WW_properties": [
      {
        "id": "COD",
        "value": 0.3,
        "unit": "kg/m3_as_O2",
        "descr": "Total chemical oxygen demand",
        "ecoinvent_id": "3f469e9e-267a-4100-9f43-4297441dc726"
      },
      {
        "id": "TKN",
        "value": 0.035,
        "unit": "kg/m3_as_N",
        "descr": "Total Kjedahl nitrogen",
        "ecoinvent_id": "98549452-463c-463d-abee-a95c2e01ade3"
      },
      {
        "id": "TP",
        "value": 0.006,
        "unit": "kg/m3_as_P",
        "descr": "Total phosphorus",
        "ecoinvent_id": "8e73d3fb-bb81-4c42-bfa6-8be4ff13125d"
      },
      {
        "id": "Ag",
        "value": 0,
        "unit": "kg/m3_as_Ag",
        "descr": "Influent Silver",
        "ecoinvent_id": "dcdc6c7b-0b72-4174-bc90-f51ed66426d5"
      },
      {
        "id": "Al",
        "value": 0.0010379,
        "unit": "kg/m3_as_Al",
        "descr": "Influent Aluminium",
        "ecoinvent_id": "77154d2e-4b05-48f2-a89a-789acd170497"
      },
      {
        "id": "As",
        "value": 9e-7,
        "unit": "kg/m3_as_As",
        "descr": "Influent Arsenic",
        "ecoinvent_id": "b321f120-4db7-4e7c-a196-82a231023052"
      },
      {
        "id": "B",
        "value": 0,
        "unit": "kg/m3_as_B",
        "descr": "Influent Boron",
        "ecoinvent_id": "c0447419-7139-44fe-a855-ea71e2b78585"
      },
      {
        "id": "Ba",
        "value": 0,
        "unit": "kg/m3_as_Ba",
        "descr": "Influent Barium",
        "ecoinvent_id": "33976f6b-2575-4410-8f60-d421bdf3e554"
      },
      {
        "id": "Be",
        "value": 0,
        "unit": "kg/m3_as_Be",
        "descr": "Influent Beryllium",
        "ecoinvent_id": "d21c7c5c-b2c2-43ae-8575-c377cc0b0495"
      },
      {
        "id": "Br",
        "value": 0,
        "unit": "kg/m3_as_Br",
        "descr": "Influent Bromine",
        "ecoinvent_id": "e4504511-88b5-4b01-a537-e049f056668c"
      },
      {
        "id": "Ca",
        "value": 0.050834000000000004,
        "unit": "kg/m3_as_Ca",
        "descr": "Influent Calcium",
        "ecoinvent_id": "ddbab0d1-b156-41bc-98e5-fb680285d7cd"
      },
      {
        "id": "Cd",
        "value": 3e-7,
        "unit": "kg/m3_as_Cd",
        "descr": "Influent Cadmium",
        "ecoinvent_id": "1111ac7e-20df-4ab4-9e02-57821894372c"
      },
      {
        "id": "Cl",
        "value": 0.030031,
        "unit": "kg/m3_as_Cl",
        "descr": "Influent Chlorine",
        "ecoinvent_id": "468e50e8-1960-4eba-bc1a-a9938a301694"
      },
      {
        "id": "Co",
        "value": 0.0000016000000000000001,
        "unit": "kg/m3_as_Co",
        "descr": "Influent Cobalt",
        "ecoinvent_id": "2f7030b9-bafc-4b43-8504-deb8b5044130"
      },
      {
        "id": "Cr",
        "value": 0.0000122,
        "unit": "kg/m3_as_Cr",
        "descr": "Influent Chromium",
        "ecoinvent_id": "bca4bb32-f701-46bb-ba1e-bad477c19f7f"
      },
      {
        "id": "Cu",
        "value": 0.0000374,
        "unit": "kg/m3_as_Cu",
        "descr": "Influent Copper",
        "ecoinvent_id": "e7451d8a-77af-44e0-86cf-ccd17ac84509"
      },
      {
        "id": "F",
        "value": 0.000032800000000000004,
        "unit": "kg/m3_as_F",
        "descr": "Influent Fluorine",
        "ecoinvent_id": "763a698f-54d7-4e2a-84a7-9cc8c0271b6a"
      },
      {
        "id": "Fe",
        "value": 0.007092800000000001,
        "unit": "kg/m3_as_Fe",
        "descr": "Influent Iron",
        "ecoinvent_id": "ebf21bca-b7cf-45d0-9d82-bfb80519a970"
      },
      {
        "id": "Hg",
        "value": 2.0000000000000002e-7,
        "unit": "kg/m3_as_Hg",
        "descr": "Influent Mercury",
        "ecoinvent_id": "a102e6f8-ebc7-450b-a39b-794be96558b7"
      },
      {
        "id": "I",
        "value": 0,
        "unit": "kg/m3_as_I",
        "descr": "Influent Iodine",
        "ecoinvent_id": "e9164ff3-fd2d-4050-895d-0e0a42317be2"
      },
      {
        "id": "K",
        "value": 0.0003989,
        "unit": "kg/m3_as_K",
        "descr": "Influent Potassium",
        "ecoinvent_id": "8b49eeb7-9caf-4101-b516-eb0aef30d530"
      },
      {
        "id": "Mg",
        "value": 0.0057071,
        "unit": "kg/m3_as_Mg",
        "descr": "Influent Magnesium",
        "ecoinvent_id": "d26c0a60-86aa-41c8-80ee-3acabc4a5095"
      },
      {
        "id": "Mn",
        "value": 0.000053,
        "unit": "kg/m3_as_Mn",
        "descr": "Influent Manganese",
        "ecoinvent_id": "8d27623b-147c-44e8-93cc-2183eac22991"
      },
      {
        "id": "Mo",
        "value": 0.000001,
        "unit": "kg/m3_as_Mo",
        "descr": "Influent Molybdenum",
        "ecoinvent_id": "aa897226-0a91-40e5-aa05-4bae3b9e4213"
      },
      {
        "id": "Na",
        "value": 0.002186,
        "unit": "kg/m3_as_Na",
        "descr": "Influent Sodium",
        "ecoinvent_id": "7b656e1b-bc07-41cd-bad4-a5b51b6287da"
      },
      {
        "id": "Ni",
        "value": 0.0000066,
        "unit": "kg/m3_as_Ni",
        "descr": "Influent Nickel",
        "ecoinvent_id": "8b574e85-ff07-46bf-a753-f1271299dcf7"
      },
      {
        "id": "Pb",
        "value": 0.0000086,
        "unit": "kg/m3_as_Pb",
        "descr": "Influent Lead",
        "ecoinvent_id": "71bc04b9-abfe-4f30-ab8f-ba654c7ad296"
      },
      {
        "id": "Sb",
        "value": 0,
        "unit": "kg/m3_as_Sb",
        "descr": "Influent Antimony",
        "ecoinvent_id": "3759d833-560a-4dbb-949e-afc63c0ade26"
      },
      {
        "id": "Sc",
        "value": 0,
        "unit": "kg/m3_as_Sc",
        "descr": "Influent Scandium",
        "ecoinvent_id": "1325d7f9-2fe2-4226-9304-ad9e5371e08f"
      },
      {
        "id": "Se",
        "value": 0,
        "unit": "kg/m3_as_Se",
        "descr": "Influent Selenium",
        "ecoinvent_id": "c35265a9-fd3e-468c-af8e-f4e020c38fc0"
      },
      {
        "id": "Si",
        "value": 0.0031263000000000003,
        "unit": "kg/m3_as_Si",
        "descr": "Influent Silicon",
        "ecoinvent_id": "67065577-4705-4ece-a892-6dd1d7ecd1e5"
      },
      {
        "id": "Sn",
        "value": 0.0000033999999999999996,
        "unit": "kg/m3_as_Sn",
        "descr": "Influent Tin",
        "ecoinvent_id": "ff888459-10c3-4700-afce-3a024aaf89cf"
      },
      {
        "id": "Sr",
        "value": 0,
        "unit": "kg/m3_as_Sr",
        "descr": "Influent Strontium",
        "ecoinvent_id": "d574cc22-07f2-4202-b564-1116ab197692"
      },
      {
        "id": "Ti",
        "value": 0,
        "unit": "kg/m3_as_Ti",
        "descr": "Influent Titanium",
        "ecoinvent_id": "abc78955-bd5f-4b1a-9607-0448dd75ebf2"
      },
      {
        "id": "Tl",
        "value": 0,
        "unit": "kg/m3_as_Tl",
        "descr": "Influent Thallium",
        "ecoinvent_id": "79baac3d-9e62-45ef-8f41-440dea32f11f"
      },
      {
        "id": "V",
        "value": 0,
        "unit": "kg/m3_as_V",
        "descr": "Influent Vanadium",
        "ecoinvent_id": "0b686a86-c506-4ad3-81fd-c3f39f05247d"
      },
      {
        "id": "W",
        "value": 0,
        "unit": "kg/m3_as_W",
        "descr": "Influent Tungsten",
        "ecoinvent_id": "058d6d50-172b-4a8a-97da-0cee759eca7d"
      },
      {
        "id": "Zn",
        "value": 0.0001094,
        "unit": "kg/m3_as_Zn",
        "descr": "Influent Zinc",
        "ecoinvent_id": "6cc518c8-4769-40df-b2cf-03f9fe00b759"
      },
      {
        "id": "BOD",
        "value": 0.14706,
        "unit": "kg/m3_as_O2",
        "descr": "Total 5d biochemical oxygen demand",
        "ecoinvent_id": "dd13a45c-ddd8-414d-821f-dfe31c7d2868"
      },
      {
        "id": "sBOD",
        "value": 0.05632,
        "unit": "kg/m3_as_O2",
        "descr": "Soluble BOD",
        "ecoinvent_id": False
      },
      {
        "id": "sCOD",
        "value": 0.1149,
        "unit": "kg/m3_as_O2",
        "descr": "Soluble COD",
        "ecoinvent_id": False
      },
      {
        "id": "bCOD",
        "value": 0.246,
        "unit": "kg/m3_as_O2",
        "descr": "Biodegradable COD (a typical value is bCOD=1.6*BOD)",
        "ecoinvent_id": False
      },
      {
        "id": "rbCOD",
        "value": 0.048,
        "unit": "kg/m3_as_O2",
        "descr": "Readily biodegradable COD (bsCOD=complex+VFA)",
        "ecoinvent_id": False
      },
      {
        "id": "VFA",
        "value": 0.0072,
        "unit": "kg/m3_as_O2",
        "descr": "Volatile Fatty Acids (Acetate)",
        "ecoinvent_id": False
      },
      {
        "id": "VSS",
        "value": 0.11569,
        "unit": "kg/m3",
        "descr": "Volatile suspended solids",
        "ecoinvent_id": False
      },
      {
        "id": "TSS",
        "value": 0.16069,
        "unit": "kg/m3",
        "descr": "Total suspended solids",
        "ecoinvent_id": "fc26822f-6400-41a5-aac6-94b7088bdabe"
      },
      {
        "id": "NH4",
        "value": 0.023100000000000002,
        "unit": "kg/m3_as_N",
        "descr": "Ammonia influent",
        "ecoinvent_id": "f7fa53fa-ee5f-4a97-bcd8-1b0851afe9a6"
      },
      {
        "id": "PO4",
        "value": 0.003,
        "unit": "kg/m3_as_P",
        "descr": "Ortophosphate influent",
        "ecoinvent_id": "7fe01cf6-6e7b-487f-b37e-32388640a8a4"
      },
      {
        "id": "Alkalinity",
        "value": 0.3,
        "unit": "kg/m3_as_CaCO3",
        "descr": "Influent alkalinity",
        "ecoinvent_id": False
      }
    ]
  },
  "outputs": {
    "chemicals": {
      "NaHCO3": {
        "value": 0,
        "unit": "kg/m3_as_NaHCO3",
        "descr": "NaHCO3 needed to maintain alkalinity"
      },
      "acrylamide": {
        "value": 0.0009291069375443328,
        "unit": "kg/m3",
        "descr": "Acrylamyde for dewatering"
      },
      "FeCl3": {
        "value": 0,
        "unit": "L/m3",
        "descr": "For chemical P removal"
      }
    },
    "electricity": {
      "value": 0.07081050141255218,
      "unit": "kWh/m3",
      "descr": "Total daily energy needed"
    },
    "CSO_amounts": [
      {
        "id": "COD_discharged_kgd",
        "value": 0.004148999999998182,
        "unit": "kg/m3_as_O2",
        "descr": "Discharged_COD_by_CSO",
        "ecoinvent_id": "fc0b5c85-3b49-42c2-a3fd-db7e57b696e3"
      },
      {
        "id": "BOD_discharged_kgd",
        "value": 0.0020337999999995304,
        "unit": "kg/m3_as_O2",
        "descr": "Discharged_BOD_by_CSO",
        "ecoinvent_id": "70d467b6-115e-43c5-add2-441de9411348"
      },
      {
        "id": "TSS_discharged_kgd",
        "value": 0.0016069000000058509,
        "unit": "kg/m3",
        "descr": "Discharged_TSS_by_CSO",
        "ecoinvent_id": "3844f446-ded5-4727-8421-17a00ef4eba7"
      },
      {
        "id": "TKN_discharged_kgd",
        "value": 0.0006353375875658429,
        "unit": "kg/m3_as_N",
        "descr": "Discharged_TKN_by_CSO",
        "ecoinvent_id": "ae70ca6c-807a-482b-9ddc-e449b4893fe3"
      },
      {
        "id": "NH4_discharged_kgd",
        "value": 0.0004620000000006286,
        "unit": "kg/m3_as_N",
        "descr": "Discharged_NH4_by_CSO",
        "ecoinvent_id": "13331e67-6006-48c4-bdb4-340c12010036"
      },
      {
        "id": "ON_discharged_kgd",
        "value": 0.00017333758756832296,
        "unit": "kg/m3_as_N",
        "descr": "Discharged_ON_by_CSO",
        "ecoinvent_id": "d43f7827-b47b-4652-8366-f370995fd206"
      },
      {
        "id": "TP_discharged_kgd",
        "value": 0.00010343849708593922,
        "unit": "kg/m3_as_P",
        "descr": "Discharged_TP_by_CSO",
        "ecoinvent_id": "b2631209-8374-431e-b7d5-56c96c6b6d79"
      },
      {
        "id": "PO4_discharged_kgd",
        "value": 0.00005999999999994898,
        "unit": "kg/m3_as_P",
        "descr": "Discharged_PO4_by_CSO",
        "ecoinvent_id": "1727b41d-377e-43cd-bc01-9eaba946eccb"
      },
      {
        "id": "OP_discharged_kgd",
        "value": 0.00004343849708610126,
        "unit": "kg/m3_as_P",
        "descr": "Discharged_OP_by_CSO",
        "ecoinvent_id": "b2631209-8374-431e-b7d5-56c96c6b6d79"
      },
      {
        "id": "elem_Al_discharged_kgd",
        "value": 0.000020758000000009602,
        "unit": "kg/m3_as_Al",
        "descr": "Al_discharged",
        "ecoinvent_id": "97e498ec-f323-4ec6-bcc0-d8a4c853bae3"
      },
      {
        "id": "elem_As_discharged_kgd",
        "value": 1.8000000000012364e-8,
        "unit": "kg/m3_as_As",
        "descr": "As_discharged",
        "ecoinvent_id": "8c8ffaa5-84ed-4668-ba7d-80fd0f47013f"
      },
      {
        "id": "elem_Ca_discharged_kgd",
        "value": 0.001016679999999326,
        "unit": "kg/m3_as_Ca",
        "descr": "Ca_discharged",
        "ecoinvent_id": "ac066c02-b403-407b-a1f0-b29ad0f8188f"
      },
      {
        "id": "elem_Cd_discharged_kgd",
        "value": 6.000000000013156e-9,
        "unit": "kg/m3_as_Cd",
        "descr": "Cd_discharged",
        "ecoinvent_id": "af83b42f-a4e6-4457-be74-46a87798f82a"
      },
      {
        "id": "elem_Cl_discharged_kgd",
        "value": 0.0006006200000001627,
        "unit": "kg/m3_as_Cl",
        "descr": "Cl_discharged",
        "ecoinvent_id": "ce312691-69ee-4cdb-9bd6-f717955b94b8"
      },
      {
        "id": "elem_Co_discharged_kgd",
        "value": 3.1999999999961747e-8,
        "unit": "kg/m3_as_Co",
        "descr": "Co_discharged",
        "ecoinvent_id": "d4291dd5-dae8-47fa-bf06-466fcecbc210"
      },
      {
        "id": "elem_Cr_discharged_kgd",
        "value": 2.4400000000080607e-7,
        "unit": "kg/m3_as_Cr",
        "descr": "Cr_discharged",
        "ecoinvent_id": "8216fc31-15a1-4d33-858f-e09650b14c63"
      },
      {
        "id": "elem_Cu_discharged_kgd",
        "value": 7.480000000018028e-7,
        "unit": "kg/m3_as_Cu",
        "descr": "Cu_discharged",
        "ecoinvent_id": "6d9550e2-e670-44c1-bad8-c0c4975ffca7"
      },
      {
        "id": "elem_F_discharged_kgd",
        "value": 6.559999999981858e-7,
        "unit": "kg/m3_as_F",
        "descr": "F_discharged",
        "ecoinvent_id": "00d2fef1-e4d4-4a16-8e81-b8cc514e4c25"
      },
      {
        "id": "elem_Fe_discharged_kgd",
        "value": 0.00014185600000038434,
        "unit": "kg/m3_as_Fe",
        "descr": "Fe_discharged",
        "ecoinvent_id": "7c335b9c-a403-47a8-bb6d-2e7d3c3a230e"
      },
      {
        "id": "elem_Hg_discharged_kgd",
        "value": 3.999999999995218e-9,
        "unit": "kg/m3_as_Hg",
        "descr": "Hg_discharged",
        "ecoinvent_id": "66bfb434-78ab-4183-b1a7-7f87d08974fa"
      },
      {
        "id": "elem_K_discharged_kgd",
        "value": 0.00000797800000001958,
        "unit": "kg/m3_as_K",
        "descr": "K_discharged",
        "ecoinvent_id": "1653bf60-f682-4088-b02d-6dc44eae2786"
      },
      {
        "id": "elem_Mg_discharged_kgd",
        "value": 0.0001141419999997062,
        "unit": "kg/m3_as_Mg",
        "descr": "Mg_discharged",
        "ecoinvent_id": "7bdab722-11d0-4c42-a099-6f9ed510a44a"
      },
      {
        "id": "elem_Mn_discharged_kgd",
        "value": 0.0000010600000000041132,
        "unit": "kg/m3_as_Mn",
        "descr": "Mn_discharged",
        "ecoinvent_id": "f532985c-90b7-46fc-aac9-b039b40e22f1"
      },
      {
        "id": "elem_Mo_discharged_kgd",
        "value": 1.9999999999989644e-8,
        "unit": "kg/m3_as_Mo",
        "descr": "Mo_discharged",
        "ecoinvent_id": "442511cc-a98b-4242-9229-5736cb9a9399"
      },
      {
        "id": "elem_Na_discharged_kgd",
        "value": 0.00004371999999996934,
        "unit": "kg/m3_as_Na",
        "descr": "Na_discharged",
        "ecoinvent_id": "1fc409bc-b8e7-48b2-92d5-2ced4aa7bae2"
      },
      {
        "id": "elem_Ni_discharged_kgd",
        "value": 1.3199999999990997e-7,
        "unit": "kg/m3_as_Ni",
        "descr": "Ni_discharged",
        "ecoinvent_id": "9798359e-a3ee-4362-a038-23a188582c6e"
      },
      {
        "id": "elem_Pb_discharged_kgd",
        "value": 1.720000000001061e-7,
        "unit": "kg/m3_as_Pb",
        "descr": "Pb_discharged",
        "ecoinvent_id": "b3ebdcc3-c588-4997-95d2-9785b26b34e1"
      },
      {
        "id": "elem_Si_discharged_kgd",
        "value": 0.00006252600000000719,
        "unit": "kg/m3_as_Si",
        "descr": "Si_discharged",
        "ecoinvent_id": "fc2371dc-5bff-41f6-a155-697fbf727b56"
      },
      {
        "id": "elem_Sn_discharged_kgd",
        "value": 6.799999999998647e-8,
        "unit": "kg/m3_as_Sn",
        "descr": "Sn_discharged",
        "ecoinvent_id": "3ddb2e36-bc1b-43a5-8ef4-cbcdbeeeea70"
      },
      {
        "id": "elem_Zn_discharged_kgd",
        "value": 0.00000218800000000019,
        "unit": "kg/m3_as_Zn",
        "descr": "Zn_discharged",
        "ecoinvent_id": "541b633c-17a3-4047-bce6-0c0e4fdb7c10"
      }
    ],
    "WWTP_influent_properties": [
      {
        "id": "COD",
        "value": 0.29585100000076636,
        "unit": "kg/m3_as_O2",
        "descr": "Total_COD",
        "ecoinvent_id": "3f469e9e-267a-4100-9f43-4297441dc726"
      },
      {
        "id": "TKN",
        "value": 0.034364662412485814,
        "unit": "kg/m3_as_N",
        "descr": "Total Kjedahl N",
        "ecoinvent_id": "98549452-463c-463d-abee-a95c2e01ade3"
      },
      {
        "id": "TP",
        "value": 0.005896561502908071,
        "unit": "kg/m3_as_P",
        "descr": "Total P",
        "ecoinvent_id": "8e73d3fb-bb81-4c42-bfa6-8be4ff13125d"
      },
      {
        "id": "BOD",
        "value": 0.1450262000003022,
        "unit": "kg/m3_as_O2",
        "descr": "Total_BOD",
        "ecoinvent_id": "dd13a45c-ddd8-414d-821f-dfe31c7d2868"
      },
      {
        "id": "sBOD",
        "value": 0.05519360000016604,
        "unit": "kg/m3_as_O2",
        "descr": "Soluble_BOD",
        "ecoinvent_id": False
      },
      {
        "id": "sCOD",
        "value": 0.112601999999697,
        "unit": "kg/m3_as_O2",
        "descr": "Soluble_COD",
        "ecoinvent_id": False
      },
      {
        "id": "bCOD",
        "value": 0.24259788657764148,
        "unit": "kg/m3_as_O2",
        "descr": "Biodegradable_COD",
        "ecoinvent_id": False
      },
      {
        "id": "rbCOD",
        "value": 0.047039999999924476,
        "unit": "kg/m3_as_O2",
        "descr": "Readily_Biodegradable_soluble_COD",
        "ecoinvent_id": False
      },
      {
        "id": "VSS",
        "value": 0.1145331000002443,
        "unit": "kg/m3",
        "descr": "Volatile Suspended Solids",
        "ecoinvent_id": False
      },
      {
        "id": "TSS",
        "value": 0.15908310000031634,
        "unit": "kg/m3",
        "descr": "Total Suspended Solids",
        "ecoinvent_id": "fc26822f-6400-41a5-aac6-94b7088bdabe"
      },
      {
        "id": "NH4",
        "value": 0.022637999999915337,
        "unit": "kg/m3_as_N",
        "descr": "Ammonia influent",
        "ecoinvent_id": "f7fa53fa-ee5f-4a97-bcd8-1b0851afe9a6"
      },
      {
        "id": "PO4",
        "value": 0.0029399999999952797,
        "unit": "kg/m3_as_P",
        "descr": "Ortophosphate influent",
        "ecoinvent_id": "7fe01cf6-6e7b-487f-b37e-32388640a8a4"
      },
      {
        "id": "Ag",
        "value": 0,
        "unit": "kg/m3_as_Ag",
        "descr": "Influent Silver",
        "ecoinvent_id": "dcdc6c7b-0b72-4174-bc90-f51ed66426d5"
      },
      {
        "id": "Al",
        "value": 0.001017141999998472,
        "unit": "kg/m3_as_Al",
        "descr": "Influent Aluminium",
        "ecoinvent_id": "77154d2e-4b05-48f2-a89a-789acd170497"
      },
      {
        "id": "As",
        "value": 8.8200000000066e-7,
        "unit": "kg/m3_as_As",
        "descr": "Influent Arsenic",
        "ecoinvent_id": "b321f120-4db7-4e7c-a196-82a231023052"
      },
      {
        "id": "B",
        "value": 0,
        "unit": "kg/m3_as_B",
        "descr": "Influent Boron",
        "ecoinvent_id": "c0447419-7139-44fe-a855-ea71e2b78585"
      },
      {
        "id": "Ba",
        "value": 0,
        "unit": "kg/m3_as_Ba",
        "descr": "Influent Barium",
        "ecoinvent_id": "33976f6b-2575-4410-8f60-d421bdf3e554"
      },
      {
        "id": "Be",
        "value": 0,
        "unit": "kg/m3_as_Be",
        "descr": "Influent Beryllium",
        "ecoinvent_id": "d21c7c5c-b2c2-43ae-8575-c377cc0b0495"
      },
      {
        "id": "Br",
        "value": 0,
        "unit": "kg/m3_as_Br",
        "descr": "Influent Bromine",
        "ecoinvent_id": "e4504511-88b5-4b01-a537-e049f056668c"
      },
      {
        "id": "Ca",
        "value": 0.0498173199998746,
        "unit": "kg/m3_as_Ca",
        "descr": "Influent Calcium",
        "ecoinvent_id": "ddbab0d1-b156-41bc-98e5-fb680285d7cd"
      },
      {
        "id": "Cd",
        "value": 2.9400000000050913e-7,
        "unit": "kg/m3_as_Cd",
        "descr": "Influent Cadmium",
        "ecoinvent_id": "1111ac7e-20df-4ab4-9e02-57821894372c"
      },
      {
        "id": "Cl",
        "value": 0.029430379999894285,
        "unit": "kg/m3_as_Cl",
        "descr": "Influent Chlorine",
        "ecoinvent_id": "468e50e8-1960-4eba-bc1a-a9938a301694"
      },
      {
        "id": "Co",
        "value": 0.0000015680000000004024,
        "unit": "kg/m3_as_Co",
        "descr": "Influent Cobalt",
        "ecoinvent_id": "2f7030b9-bafc-4b43-8504-deb8b5044130"
      },
      {
        "id": "Cr",
        "value": 0.00001195599999997965,
        "unit": "kg/m3_as_Cr",
        "descr": "Influent Chromium",
        "ecoinvent_id": "bca4bb32-f701-46bb-ba1e-bad477c19f7f"
      },
      {
        "id": "Cu",
        "value": 0.000036652000000025886,
        "unit": "kg/m3_as_Cu",
        "descr": "Influent Copper",
        "ecoinvent_id": "e7451d8a-77af-44e0-86cf-ccd17ac84509"
      },
      {
        "id": "F",
        "value": 0.00003214400000006723,
        "unit": "kg/m3_as_F",
        "descr": "Influent Fluorine",
        "ecoinvent_id": "763a698f-54d7-4e2a-84a7-9cc8c0271b6a"
      },
      {
        "id": "Fe",
        "value": 0.006950943999981973,
        "unit": "kg/m3_as_Fe",
        "descr": "Influent Iron",
        "ecoinvent_id": "ebf21bca-b7cf-45d0-9d82-bfb80519a970"
      },
      {
        "id": "Hg",
        "value": 1.960000000000503e-7,
        "unit": "kg/m3_as_Hg",
        "descr": "Influent Mercury",
        "ecoinvent_id": "a102e6f8-ebc7-450b-a39b-794be96558b7"
      },
      {
        "id": "I",
        "value": 0,
        "unit": "kg/m3_as_I",
        "descr": "Influent Iodine",
        "ecoinvent_id": "e9164ff3-fd2d-4050-895d-0e0a42317be2"
      },
      {
        "id": "K",
        "value": 0.0003909219999993496,
        "unit": "kg/m3_as_K",
        "descr": "Influent Potassium",
        "ecoinvent_id": "8b49eeb7-9caf-4101-b516-eb0aef30d530"
      },
      {
        "id": "Mg",
        "value": 0.0055929579999940415,
        "unit": "kg/m3_as_Mg",
        "descr": "Influent Magnesium",
        "ecoinvent_id": "d26c0a60-86aa-41c8-80ee-3acabc4a5095"
      },
      {
        "id": "Mn",
        "value": 0.000051940000000083586,
        "unit": "kg/m3_as_Mn",
        "descr": "Influent Manganese",
        "ecoinvent_id": "8d27623b-147c-44e8-93cc-2183eac22991"
      },
      {
        "id": "Mo",
        "value": 9.800000000011189e-7,
        "unit": "kg/m3_as_Mo",
        "descr": "Influent Molybdenum",
        "ecoinvent_id": "aa897226-0a91-40e5-aa05-4bae3b9e4213"
      },
      {
        "id": "Na",
        "value": 0.002142280000001051,
        "unit": "kg/m3_as_Na",
        "descr": "Influent Sodium",
        "ecoinvent_id": "7b656e1b-bc07-41cd-bad4-a5b51b6287da"
      },
      {
        "id": "Ni",
        "value": 0.000006467999999981711,
        "unit": "kg/m3_as_Ni",
        "descr": "Influent Nickel",
        "ecoinvent_id": "8b574e85-ff07-46bf-a753-f1271299dcf7"
      },
      {
        "id": "Pb",
        "value": 0.000008428000000004765,
        "unit": "kg/m3_as_Pb",
        "descr": "Influent Lead",
        "ecoinvent_id": "71bc04b9-abfe-4f30-ab8f-ba654c7ad296"
      },
      {
        "id": "Sb",
        "value": 0,
        "unit": "kg/m3_as_Sb",
        "descr": "Influent Antimony",
        "ecoinvent_id": "3759d833-560a-4dbb-949e-afc63c0ade26"
      },
      {
        "id": "Sc",
        "value": 0,
        "unit": "kg/m3_as_Sc",
        "descr": "Influent Scandium",
        "ecoinvent_id": "1325d7f9-2fe2-4226-9304-ad9e5371e08f"
      },
      {
        "id": "Se",
        "value": 0,
        "unit": "kg/m3_as_Se",
        "descr": "Influent Selenium",
        "ecoinvent_id": "c35265a9-fd3e-468c-af8e-f4e020c38fc0"
      },
      {
        "id": "Si",
        "value": 0.0030637739999832547,
        "unit": "kg/m3_as_Si",
        "descr": "Influent Silicon",
        "ecoinvent_id": "67065577-4705-4ece-a892-6dd1d7ecd1e5"
      },
      {
        "id": "Sn",
        "value": 0.0000033320000000086614,
        "unit": "kg/m3_as_Sn",
        "descr": "Influent Tin",
        "ecoinvent_id": "ff888459-10c3-4700-afce-3a024aaf89cf"
      },
      {
        "id": "Sr",
        "value": 0,
        "unit": "kg/m3_as_Sr",
        "descr": "Influent Strontium",
        "ecoinvent_id": "d574cc22-07f2-4202-b564-1116ab197692"
      },
      {
        "id": "Ti",
        "value": 0,
        "unit": "kg/m3_as_Ti",
        "descr": "Influent Titanium",
        "ecoinvent_id": "abc78955-bd5f-4b1a-9607-0448dd75ebf2"
      },
      {
        "id": "Tl",
        "value": 0,
        "unit": "kg/m3_as_Tl",
        "descr": "Influent Thallium",
        "ecoinvent_id": "79baac3d-9e62-45ef-8f41-440dea32f11f"
      },
      {
        "id": "V",
        "value": 0,
        "unit": "kg/m3_as_V",
        "descr": "Influent Vanadium",
        "ecoinvent_id": "0b686a86-c506-4ad3-81fd-c3f39f05247d"
      },
      {
        "id": "W",
        "value": 0,
        "unit": "kg/m3_as_W",
        "descr": "Influent Tungsten",
        "ecoinvent_id": "058d6d50-172b-4a8a-97da-0cee759eca7d"
      },
      {
        "id": "Zn",
        "value": 0.00010721200000007869,
        "unit": "kg/m3_as_Zn",
        "descr": "Influent Zinc",
        "ecoinvent_id": "6cc518c8-4769-40df-b2cf-03f9fe00b759"
      }
    ],
    "WWTP_emissions_water": [
      {
        "id": "COD_effluent_water",
        "value": 0.021945025037508458,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "fc0b5c85-3b49-42c2-a3fd-db7e57b696e3"
      },
      {
        "id": "TKN_effluent_water",
        "value": 0.0188551724194549,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "ae70ca6c-807a-482b-9ddc-e449b4893fe3"
      },
      {
        "id": "TP_effluent_water",
        "value": 0.002907336791002308,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "b2631209-8374-431e-b7d5-56c96c6b6d79"
      },
      {
        "id": "Al_effluent_water",
        "value": 0.000050857099999802815,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "97e498ec-f323-4ec6-bcc0-d8a4c853bae3"
      },
      {
        "id": "As_effluent_water",
        "value": 6.87960000000487e-7,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "8c8ffaa5-84ed-4668-ba7d-80fd0f47013f"
      },
      {
        "id": "Ca_effluent_water",
        "value": 0.04483558800001629,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "ac066c02-b403-407b-a1f0-b29ad0f8188f"
      },
      {
        "id": "Cd_effluent_water",
        "value": 1.4700000000011925e-7,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "af83b42f-a4e6-4457-be74-46a87798f82a"
      },
      {
        "id": "Cl_effluent_water",
        "value": 0.029430379999917933,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "ce312691-69ee-4cdb-9bd6-f717955b94b8"
      },
      {
        "id": "Co_effluent_water",
        "value": 7.839999999994518e-7,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "d4291dd5-dae8-47fa-bf06-466fcecbc210"
      },
      {
        "id": "Cr_effluent_water",
        "value": 0.000005977999999998929,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "8216fc31-15a1-4d33-858f-e09650b14c63"
      },
      {
        "id": "Cu_effluent_water",
        "value": 0.00000916300000000092,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "6d9550e2-e670-44c1-bad8-c0c4975ffca7"
      },
      {
        "id": "F_effluent_water",
        "value": 0.000032144000000016604,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "00d2fef1-e4d4-4a16-8e81-b8cc514e4c25"
      },
      {
        "id": "Fe_effluent_water",
        "value": 0.0034754719999909867,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "7c335b9c-a403-47a8-bb6d-2e7d3c3a230e"
      },
      {
        "id": "Hg_effluent_water",
        "value": 5.879999999991447e-8,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "66bfb434-78ab-4183-b1a7-7f87d08974fa"
      },
      {
        "id": "K_effluent_water",
        "value": 0.0003909220000005007,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "1653bf60-f682-4088-b02d-6dc44eae2786"
      },
      {
        "id": "Mg_effluent_water",
        "value": 0.005033662200003164,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "7bdab722-11d0-4c42-a099-6f9ed510a44a"
      },
      {
        "id": "Mn_effluent_water",
        "value": 0.00002597000000002936,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "f532985c-90b7-46fc-aac9-b039b40e22f1"
      },
      {
        "id": "Mo_effluent_water",
        "value": 4.900000000009896e-7,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "442511cc-a98b-4242-9229-5736cb9a9399"
      },
      {
        "id": "Na_effluent_water",
        "value": 0.002142280000000028,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "1fc409bc-b8e7-48b2-92d5-2ced4aa7bae2"
      },
      {
        "id": "Ni_effluent_water",
        "value": 0.000003880799999976148,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "9798359e-a3ee-4362-a038-23a188582c6e"
      },
      {
        "id": "Pb_effluent_water",
        "value": 8.428000000009206e-7,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "b3ebdcc3-c588-4997-95d2-9785b26b34e1"
      },
      {
        "id": "Si_effluent_water",
        "value": 0.00015318870000010065,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "fc2371dc-5bff-41f6-a155-697fbf727b56"
      },
      {
        "id": "Sn_effluent_water",
        "value": 0.0000013661200000001373,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "3ddb2e36-bc1b-43a5-8ef4-cbcdbeeeea70"
      },
      {
        "id": "Zn_effluent_water",
        "value": 0.000032163599999989854,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "541b633c-17a3-4047-bce6-0c0e4fdb7c10"
      }
    ],
    "WWTP_emissions_air": [
      {
        "id": "COD_effluent_air",
        "value": 0.09571109554870054,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": False
      },
      {
        "id": "CO2_effluent_air",
        "value": 0.12080153406783939,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": False
      }
    ],
    "WWTP_emissions_sludge": [
      {
        "id": "COD_effluent_sludge",
        "value": 0.09805841706413776,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": False
      },
      {
        "id": "TKN_effluent_sludge",
        "value": 0.007699532826110953,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": False
      },
      {
        "id": "TP_effluent_sludge",
        "value": 0.0010201547509641386,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": False
      },
      {
        "id": "Al_effluent_sludge",
        "value": 0.0009662848999978451,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "e9688cbc-7400-457a-a936-5ab123ea326c"
      },
      {
        "id": "As_effluent_sludge",
        "value": 1.9404000000022847e-7,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "30f0aa15-2d50-4f09-af94-683b6dd68adc"
      },
      {
        "id": "Ca_effluent_sludge",
        "value": 0.0049817320000001926,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "f9da385d-5b1b-4548-826c-0bf5892a9fd9"
      },
      {
        "id": "Cd_effluent_sludge",
        "value": 1.4700000000011925e-7,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "ad7781c7-5dc2-4421-b182-e1fd4cef7fa5"
      },
      {
        "id": "Co_effluent_sludge",
        "value": 7.839999999994518e-7,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "66e996b5-5f7b-449f-8893-0b787af21d7e"
      },
      {
        "id": "Cr_effluent_sludge",
        "value": 0.000005977999999998929,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "e1d2c19b-3a97-4f52-a83f-fe88400452c2"
      },
      {
        "id": "Cu_effluent_sludge",
        "value": 0.000027489000000059605,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "0132d97c-5f19-4397-9197-59ab801b10cf"
      },
      {
        "id": "Fe_effluent_sludge",
        "value": 0.0034754719999909867,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "d8364dfc-5753-4585-bf50-4d42b126f72d"
      },
      {
        "id": "Hg_effluent_sludge",
        "value": 1.3719999999972642e-7,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "2a256b0b-6003-4669-a3c1-1d3eba2de45e"
      },
      {
        "id": "Mg_effluent_sludge",
        "value": 0.0005592957999997452,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "8aedc313-f49b-42cd-8d54-fc877ec03017"
      },
      {
        "id": "Mn_effluent_sludge",
        "value": 0.00002597000000002936,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "2bc683e4-3780-4f00-8c1d-fd53e05cfde7"
      },
      {
        "id": "Mo_effluent_sludge",
        "value": 4.900000000009896e-7,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "83f67a9e-bf78-4e0d-b1f0-5051a1fda9fe"
      },
      {
        "id": "Ni_effluent_sludge",
        "value": 0.0000025871999999935723,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "f767b36f-62bf-4458-b694-ecbefd2ab970"
      },
      {
        "id": "Pb_effluent_sludge",
        "value": 0.000007585199999994075,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "e5507d89-78ad-4746-900c-b9afa5a62ea6"
      },
      {
        "id": "Si_effluent_sludge",
        "value": 0.0029105852999928173,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "dd7e15dc-c438-43f7-9c0d-d0a627163cf1"
      },
      {
        "id": "Sn_effluent_sludge",
        "value": 0.0000019658800000001973,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "d8551abf-da96-4429-846b-0973136b7d48"
      },
      {
        "id": "Zn_effluent_sludge",
        "value": 0.00007504840000001422,
        "unit": "kg/m3",
        "descr": "",
        "ecoinvent_id": "33f96fe7-39da-47ca-837f-f2c311681d1b"
      }
    ],
    "sludge_properties": [
      {
        "id": "TSS_removed_kgd",
        "value": 0.0811206076932649,
        "unit": "kg/m3_as_TSS",
        "descr": "Primary_settler_sludge_produced_per_day",
        "ecoinvent_id": False
      },
      {
        "id": "VSS_removed_kgd",
        "value": 0.04993560769321448,
        "unit": "kg/m3_as_VSS",
        "descr": "Primary_settler_VSS_produced_per_day",
        "ecoinvent_id": False
      },
      {
        "id": "P_X_TSS",
        "value": 0.09291069375422012,
        "unit": "kg/m3_as_TSS",
        "descr": "Total_sludge_produced_per_day",
        "ecoinvent_id": False
      },
      {
        "id": "P_X_VSS",
        "value": 0.0688505499990697,
        "unit": "kg/m3_as_VSS",
        "descr": "Volatile suspended solids produced per day",
        "ecoinvent_id": False
      },
      {
        "id": "sludge_primary_C_content",
        "value": 0.025467159923550753,
        "unit": "kg/m3_as_C",
        "descr": "",
        "ecoinvent_id": False
      },
      {
        "id": "sludge_primary_H_content",
        "value": 0.004204008164890638,
        "unit": "kg/m3_as_H",
        "descr": "",
        "ecoinvent_id": "2d23d1bb-e137-4ade-83fc-fbd0421e6cd5"
      },
      {
        "id": "sludge_primary_O_content",
        "value": 0.015965085366076437,
        "unit": "kg/m3_as_O",
        "descr": "",
        "ecoinvent_id": "dbf41b1b-c7b8-4d5e-b39c-f858eb868df5"
      },
      {
        "id": "sludge_primary_N_content",
        "value": 0.0037381626463286466,
        "unit": "kg/m3_as_N",
        "descr": "",
        "ecoinvent_id": "f53a5dbc-3bd3-4570-adff-b00790ea3ffc"
      },
      {
        "id": "sludge_primary_P_content",
        "value": 0.0005611915923253719,
        "unit": "kg/m3_as_P",
        "descr": "",
        "ecoinvent_id": "97f3bbfe-fa3a-4d05-9cb6-bb4b6379c5ef"
      },
      {
        "id": "sludge_primary_water_content",
        "value": 0.2433618230788852,
        "unit": "kg/m3_as_H2O",
        "descr": "Primary sludge water content",
        "ecoinvent_id": "a9358458-9724-4f03-b622-106eda248916"
      },
      {
        "id": "sludge_secondary_C_content",
        "value": 0.03511378049961422,
        "unit": "kg/m3_as_C",
        "descr": "",
        "ecoinvent_id": False
      },
      {
        "id": "sludge_secondary_H_content",
        "value": 0.004600436519268669,
        "unit": "kg/m3_as_H",
        "descr": "",
        "ecoinvent_id": "2d23d1bb-e137-4ade-83fc-fbd0421e6cd5"
      },
      {
        "id": "sludge_secondary_O_content",
        "value": 0.019841508730394253,
        "unit": "kg/m3_as_O",
        "descr": "",
        "ecoinvent_id": "dbf41b1b-c7b8-4d5e-b39c-f858eb868df5"
      },
      {
        "id": "sludge_secondary_N_content",
        "value": 0.00826206599990087,
        "unit": "kg/m3_as_N",
        "descr": "",
        "ecoinvent_id": "f53a5dbc-3bd3-4570-adff-b00790ea3ffc"
      },
      {
        "id": "sludge_secondary_P_content",
        "value": 0.0010327582499876087,
        "unit": "kg/m3_as_P",
        "descr": "",
        "ecoinvent_id": "97f3bbfe-fa3a-4d05-9cb6-bb4b6379c5ef"
      },
      {
        "id": "sludge_secondary_water_content",
        "value": 0.2787320812622056,
        "unit": "kg/m3_as_H2O",
        "descr": "Secondary sludge water content",
        "ecoinvent_id": "a9358458-9724-4f03-b622-106eda248916"
      }
    ],
    "untreated_as_emissions": [
      {
        "id": "COD",
        "value": 0.3,
        "unit": "kg/m3_as_O2",
        "descr": "untreated as emission for COD",
        "ecoinvent_id": "fc0b5c85-3b49-42c2-a3fd-db7e57b696e3"
      },
      {
        "id": "BOD",
        "value": 0.14706,
        "unit": "kg/m3_as_O2",
        "descr": "untreated as emission for BOD",
        "ecoinvent_id": "70d467b6-115e-43c5-add2-441de9411348"
      },
      {
        "id": "TSS",
        "value": 0.16069,
        "unit": "kg/m3",
        "descr": "untreated as emission for TSS",
        "ecoinvent_id": "3844f446-ded5-4727-8421-17a00ef4eba7"
      },
      {
        "id": "TKN",
        "value": 0.035,
        "unit": "kg/m3_as_N",
        "descr": "untreated as emission for TKN",
        "ecoinvent_id": "ae70ca6c-807a-482b-9ddc-e449b4893fe3"
      },
      {
        "id": "NH4",
        "value": 0.023100000000000002,
        "unit": "kg/m3_as_N",
        "descr": "untreated as emission for NH4",
        "ecoinvent_id": "13331e67-6006-48c4-bdb4-340c12010036"
      },
      {
        "id": "ON",
        "value": 0.011899999999999999,
        "unit": "kg/m3_as_N",
        "descr": "untreated as emission for ON",
        "ecoinvent_id": "d43f7827-b47b-4652-8366-f370995fd206"
      },
      {
        "id": "TP",
        "value": 0.006,
        "unit": "kg/m3_as_P",
        "descr": "untreated as emission for TP",
        "ecoinvent_id": "b2631209-8374-431e-b7d5-56c96c6b6d79"
      },
      {
        "id": "PO4",
        "value": 0.003,
        "unit": "kg/m3_as_P",
        "descr": "untreated as emission for PO4",
        "ecoinvent_id": "1727b41d-377e-43cd-bc01-9eaba946eccb"
      },
      {
        "id": "OP",
        "value": 0.003,
        "unit": "kg/m3_as_P",
        "descr": "untreated as emission for OP",
        "ecoinvent_id": "b2631209-8374-431e-b7d5-56c96c6b6d79"
      },
      {
        "id": "Al",
        "value": 0.0010379,
        "unit": "kg/m3_as_Al",
        "descr": "untreated as emission for Al",
        "ecoinvent_id": "97e498ec-f323-4ec6-bcc0-d8a4c853bae3"
      },
      {
        "id": "As",
        "value": 9e-7,
        "unit": "kg/m3_as_As",
        "descr": "untreated as emission for As",
        "ecoinvent_id": "8c8ffaa5-84ed-4668-ba7d-80fd0f47013f"
      },
      {
        "id": "Ca",
        "value": 0.050834000000000004,
        "unit": "kg/m3_as_Ca",
        "descr": "untreated as emission for Ca",
        "ecoinvent_id": "ac066c02-b403-407b-a1f0-b29ad0f8188f"
      },
      {
        "id": "Cd",
        "value": 3e-7,
        "unit": "kg/m3_as_Cd",
        "descr": "untreated as emission for Cd",
        "ecoinvent_id": "af83b42f-a4e6-4457-be74-46a87798f82a"
      },
      {
        "id": "Cl",
        "value": 0.030031,
        "unit": "kg/m3_as_Cl",
        "descr": "untreated as emission for Cl",
        "ecoinvent_id": "ce312691-69ee-4cdb-9bd6-f717955b94b8"
      },
      {
        "id": "Co",
        "value": 0.0000016000000000000001,
        "unit": "kg/m3_as_Co",
        "descr": "untreated as emission for Co",
        "ecoinvent_id": "d4291dd5-dae8-47fa-bf06-466fcecbc210"
      },
      {
        "id": "Cr",
        "value": 0.0000122,
        "unit": "kg/m3_as_Cr",
        "descr": "untreated as emission for Cr",
        "ecoinvent_id": "8216fc31-15a1-4d33-858f-e09650b14c63"
      },
      {
        "id": "Cu",
        "value": 0.0000374,
        "unit": "kg/m3_as_Cu",
        "descr": "untreated as emission for Cu",
        "ecoinvent_id": "6d9550e2-e670-44c1-bad8-c0c4975ffca7"
      },
      {
        "id": "F",
        "value": 0.000032800000000000004,
        "unit": "kg/m3_as_F",
        "descr": "untreated as emission for F",
        "ecoinvent_id": "00d2fef1-e4d4-4a16-8e81-b8cc514e4c25"
      },
      {
        "id": "Fe",
        "value": 0.007092800000000001,
        "unit": "kg/m3_as_Fe",
        "descr": "untreated as emission for Fe",
        "ecoinvent_id": "7c335b9c-a403-47a8-bb6d-2e7d3c3a230e"
      },
      {
        "id": "Hg",
        "value": 2.0000000000000002e-7,
        "unit": "kg/m3_as_Hg",
        "descr": "untreated as emission for Hg",
        "ecoinvent_id": "66bfb434-78ab-4183-b1a7-7f87d08974fa"
      },
      {
        "id": "K",
        "value": 0.0003989,
        "unit": "kg/m3_as_K",
        "descr": "untreated as emission for K",
        "ecoinvent_id": "1653bf60-f682-4088-b02d-6dc44eae2786"
      },
      {
        "id": "Mg",
        "value": 0.0057071,
        "unit": "kg/m3_as_Mg",
        "descr": "untreated as emission for Mg",
        "ecoinvent_id": "7bdab722-11d0-4c42-a099-6f9ed510a44a"
      },
      {
        "id": "Mn",
        "value": 0.000053,
        "unit": "kg/m3_as_Mn",
        "descr": "untreated as emission for Mn",
        "ecoinvent_id": "f532985c-90b7-46fc-aac9-b039b40e22f1"
      },
      {
        "id": "Mo",
        "value": 0.000001,
        "unit": "kg/m3_as_Mo",
        "descr": "untreated as emission for Mo",
        "ecoinvent_id": "442511cc-a98b-4242-9229-5736cb9a9399"
      },
      {
        "id": "Na",
        "value": 0.002186,
        "unit": "kg/m3_as_Na",
        "descr": "untreated as emission for Na",
        "ecoinvent_id": "1fc409bc-b8e7-48b2-92d5-2ced4aa7bae2"
      },
      {
        "id": "Ni",
        "value": 0.0000066,
        "unit": "kg/m3_as_Ni",
        "descr": "untreated as emission for Ni",
        "ecoinvent_id": "9798359e-a3ee-4362-a038-23a188582c6e"
      },
      {
        "id": "Pb",
        "value": 0.0000086,
        "unit": "kg/m3_as_Pb",
        "descr": "untreated as emission for Pb",
        "ecoinvent_id": "b3ebdcc3-c588-4997-95d2-9785b26b34e1"
      },
      {
        "id": "Si",
        "value": 0.0031263000000000003,
        "unit": "kg/m3_as_Si",
        "descr": "untreated as emission for Si",
        "ecoinvent_id": "fc2371dc-5bff-41f6-a155-697fbf727b56"
      },
      {
        "id": "Sn",
        "value": 0.0000033999999999999996,
        "unit": "kg/m3_as_Sn",
        "descr": "untreated as emission for Sn",
        "ecoinvent_id": "3ddb2e36-bc1b-43a5-8ef4-cbcdbeeeea70"
      },
      {
        "id": "Zn",
        "value": 0.0001094,
        "unit": "kg/m3_as_Zn",
        "descr": "untreated as emission for Zn",
        "ecoinvent_id": "541b633c-17a3-4047-bce6-0c0e4fdb7c10"
      }
    ]
  }
}

#debug: print input string
#parse json
#received_string = sys.argv[1].encode('ascii','ignore').decode('ascii')
#received_json = json.loads(received_string)

#print('parsed JSON object: ',json.dumps(received_json, indent=4, sort_keys=True))

'''pretty printer (debug)'''
pp=pprint.PrettyPrinter(indent=2)
#pp.pprint(received_json)

'''args conversion'''
args = {k: v for d in from_tool.values() for k, v in d.items()}
result = {}

if args['untreated_fraction'] == 0:
  result['untreated'] = False;
else:
  untreated = DirectDischarge_ecoSpold(root_dir, **args)
  result['untreated'] = untreated.generate_ecoSpold2()

if args['untreated_fraction'] == 1:
  result['treated'] = False;
else:
  treated = WWT_ecoSpold(root_dir, **args)
  result['treated'] = treated.generate_ecoSpold2()

#pp.pprint(result)
#show html links
print("<hr><b style=color:green>Success!</b><ul>")
if result['untreated']:
  print('<li><a target=_blank href="wastewater_treatment_tool/output/'+result['untreated'][1]+'">Click here to download',result['untreated'][1]+"</a>")
else:
  print("<li>No direct discharge dataset ecoSpold was generated because 100% of wastewater sent to the sewer system is treated in this region.")
if result['treated']:
  print('<li><a target=_blank href="wastewater_treatment_tool/output/'+result['treated'][1]+'">Click here to download',result['treated'][1]+"</a>")
else:
  print("<li>No treatment dataset ecoSpold was generated because 100% of wastewater sent to the sewer system is dischaged to the environment without treatment.")
print("</ul>")