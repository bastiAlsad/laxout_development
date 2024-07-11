from django.shortcuts import render
from django.db import models as modelsdb
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from django.http import HttpResponse
import json


####befund logik
@login_required(login_url="login")
def befund(request, id=None):
    test_list_json = request.POST.get("test_list")
    if test_list_json:
        test_list = json.loads(
            test_list_json
        )  # Decode the JSON string to a Python list
        models.StandartBefund.objects.get_or_create(
            created_by=request.user, created_for=id
        )
        models.Befund.objects.get_or_create(created_for=id, befund="standart_befund")
        for test in test_list:
            if test == "fragenevaluation_icf":
                models.FragenevaluationNachICFKategorien.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="fragenevaluation_icf"
                )
            if test == "fragenevaluation_bio_psycho_sozial_krankheitsmodell":
                models.FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id,
                    befund="fragenevaluation_bio_psycho_sozial_krankheitsmodell",
                )
            if test == "w_fragen":
                models.FragenevaluationenNachDen7WFragen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="w_fragen")
            if test == "stand_reha_phase":
                models.StandDerReHaPhase.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="stand_reha_phase")
            if test == "nebenerkrankungen_medikamente":
                models.NebenerkrankungenMedikamente.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="nebenerkrankungen_medikamente"
                )
            if test == "historia_morbis":
                models.HistoriaMorbis.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="historia_morbis")

            if test == "nrs_numeric_rating_scale":
                models.NrsNumericRatingScale.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="nrs_numeric_rating_scale"
                )
            if test == "aktive_beweglichkeit":
                models.AktiveBeweglichkeit.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="aktive_beweglichkeit"
                )
            if test == "passive_beweglichkeit":
                models.PassiveBeweglichkeit.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="passive_beweglichkeit"
                )
            if test == "beweglichkeitsmessung":
                models.BeweglichkeitsmessungKnie.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="beweglichkeitsmessung"
                )
            if test == "isometrischer_krafttest":
                models.IsometrischerKrafttest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="isometrischer_krafttest"
                )
            if test == "muskelfunktionspruefung":
                models.Muskelfunktionspruefung.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="muskelfunktionspruefung"
                )
            if test == "einbeinstand_60_sekunden":
                models.Einbeinstand60Sekunden.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="einbeinstand_60_sekunden"
                )
            if test == "einbeinstand_30_sekunden_geschlossene_augen":
                models.Einbeinstand30SekundenGeschlosseneAugen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="einbeinstand_30_sekunden_geschlossene_augen"
                )
            if test == "alltagsfunktionen":
                models.Alltagsfunktionen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="alltagsfunktionen")
            if test == "beinlaengenmessung":
                models.Beinlaengenmessung.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="beinlaengenmessung"
                )
            if test == "quadriceps_dehnungstest":
                models.QuadricepsDehnungstest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="quadriceps_dehnungstest"
                )
            if test == "m_rectus_dehnungstest":
                models.MRectusDehnungstest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="m_rectus_dehnungstest"
                )
            if test == "hamstringtest":
                models.Hamstringtest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="hamstringtest")
            if test == "umfangsmessung":
                models.Umfangsmessung.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="umfangsmessung")
            if test == "tanzende_patella":
                models.TanzendePatella.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="tanzende_patella")
            if test == "mini_erguss_test":
                models.MiniErgussTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="mini_erguss_test")
            if test == "glide_test":
                models.GlideTest.objects.create(created_by=request.user, created_for=id)
                models.Befund.objects.create(created_for=id, befund="glide_test")
            if test == "tilt_test":
                models.TiltTest.objects.create(created_by=request.user, created_for=id)
                models.Befund.objects.create(created_for=id, befund="tilt_test")
            if test == "aprehension_test":
                models.AprehensionTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="aprehension_test")
            if test == "zohlen_zeichen":
                models.ZohlenZeichen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="zohlen_zeichen")
            if test == "facettendruckschmerztest":
                models.Facettendruckschmerztest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="facettendruckschmerztest"
                )
            if test == "valgus_test":
                models.ValgusTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="valgus_test")
            if test == "varus_test":
                models.VarusTest.objects.create(created_by=request.user, created_for=id)
                models.Befund.objects.create(created_for=id, befund="varus_test")
            if test == "lachmann_test":
                models.LachmannTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="lachmann_test")
            if test == "vordere_schublade":
                models.VordereSchublade.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="vordere_schublade")
            if test == "pivot_shift_test":
                models.PivotShiftTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="pivot_shift_test")
            if test == "hintere_schublade":
                models.HintereSchublade.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="hintere_schublade")
            if test == "gravitiy_sign":
                models.GravitiySign.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="gravitiy_sign")
            if test == "loomers_test":
                models.LoomersTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="loomers_test")
            if test == "steinmann1":
                models.Steinmann1.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="steinmann1")
            if test == "steinmann3":
                models.Steinmann3.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="steinmann3")
            if test == "theslay_test":
                models.TheslayTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="theslayTest")
            if test == "mac_murray_test":
                models.MacMurrayTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="mac_murray_test")
            if test == "payr_zeichen":
                models.PayrZeichen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="payr_zeichen")
            if test == "apley_zeichen":
                models.ApleyZeichen.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="apley_zeichen")
            if test == "medio_patellarer_plica_test":
                models.MedioPatellarerPlicaTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="medio_patellarer_plica_test"
                )
            if test == "hughston_plica_test":
                models.HughstonPlicaTest.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="hughston_plica_test"
                )
            if test == "red_flag_screening_schulter":
                models.RedFlagScreeningSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="red_flag_screening_schulter"
                )
            if test == "aktive_beweglichkeit_schulter":
                models.AktiveBeweglichkeitSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="aktive_beweglichkeit_schulter"
                )
            if test == "passive_beweglichkeit_schulter":
                models.PassiveBeweglichkeitSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="passive_beweglichkeit_schulter"
                )
            if test == "beweglichkeitsmessung_schulter":
                models.BeweglichkeitsmessungSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="beweglichkeitsmessung_schulter"
                )
            if test == "c_sar":
                models.CopenhagenShoulderAbductionRating.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="c_sar")
            if test == "posteriore_schultersteifheit":
                models.PosterioreSchultersteifheit.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="posteriore_schultersteifheit"
                )
            if test == "isometrischer_krafttest_schulter":
                models.IsometrischerKrafttestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="isometrischer_krafttest_schulter"
                )
            if test == "muskelfunktionspruefung_schulter":
                models.MuskelfunktionspruefungSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="muskelfunktionspruefung_schulter"
                )
            if test == "feds_kalassifikation":
                models.FEDSKalassifikationSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="feds_kalassifikation"
                )
            if test == "anterior_aprehension_test":
                models.AnteriorAprehensionTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="anterior_aprehension_test"
                )
            if test == "relocation_test_nach_jobe":
                models.RelocationTestnachJobeSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="relocation_test_nach_jobe"
                )
            if test == "surprise_release_test":
                models.SurpriseReleaseTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="surprise_release_test"
                )
            if test == "anterior_drawer_test":
                models.AnteriorDrawerTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="anterior_drawer_test"
                )
            if test == "sulcustest":
                models.SulcusTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="sulcustest")
            if test == "posterior_aprehension_test":
                models.PosteriorAprehensionTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="posterior_aprehension_test"
                )
            if test == "jerk_test":
                models.JerkTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="jerk_test")
            if test == "kim_test":
                models.KimTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="kim_test")
            if test == "load_and_shift_test":
                models.LoadAndShiftTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="load_and_shift_test"
                )
            if test == "sulcus_zeichen":
                models.SulcusZeichenSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="sulcus_zeichen")
            if test == "coudance_walch_test":
                models.CoudanceWalchTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="coudance_walch_test"
                )
            if test == "gargey_test":
                models.GargeyTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="gargey_test")
            if test == "nervenmobilitaetstestungen_bpnt":
                models.NervenmobilitaetstestungenSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="nervenmobilitaetstestungen_bpnt"
                )
            if test == "schnell_anamnese_frozen_shoulder":
                models.SchnellAnamneseFrozenShoulder.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="schnell_anamnese_frozen_shoulder"
                )
            if test == "adsons_test":
                models.AdsonsTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="adsons_test")
            if test == "wrights_test":
                models.WrightsTestHyperabduktionSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="wrights_test")
            if test == "edens_test":
                models.EdensTestCostoclavikulaererDruckSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="edens_test")
            if test == "east_test":
                models.ElevatedArmStressTestEASTSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="east_test")
            if test == "cyrax_release_test":
                models.CyraxReleaseTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="cyrax_release_test"
                )
            if test == "morley_compression_test":
                models.MorleyCmpressionTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="morley_compression_test"
                )
            if test == "irritierbarkeit_schulter_star":
                models.IrritierbarkeitderSchulterAnlehnungSTASchulterDiagnose.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="irritierbarkeit_schulter_star"
                )
            if test == "alltagsfunktionen_schulter":
                models.AlltagsfunktionenSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="alltagsfunktionen_schulter"
                )
            if test == "umfangsmessung_arm":
                models.UmfangsmessungArm.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="umfangsmessung_arm"
                )
            if test == "scapula_assistenstest_sat":
                models.ScapulaAssistenstesSATSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="scapula_assistenstest_sat"
                )
            if test == "lateral_scapula_slide_test":
                models.LateralerScapulaSlideTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="lateral_scapula_slide_test"
                )
            if test == "scapula_retraction_test_srt":
                models.ScapulaRetractionTestSRTSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="scapula_retraction_test_srt"
                )
            if test == "lateraler_scapula_slide_test":
                models.LateralerScapulaSlideTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="lateraler_scapula_slide_test"
                )
            if test == "jobe_test":
                models.JobeTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="jobe_test")
            if test == "null_grad_adduktionstest":
                models.NullGradAdduktionstestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="null_grad_adduktionstest"
                )
            if test == "drop_arm_zeichen":
                models.DropArmZeichenSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="drop_arm_zeichen")
            if test == "lift_off_test":
                models.LiftOffTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="lift_off_test")
            if test == "belly_press_belly_off_zeichen":
                models.BellyPressBellyOffZeichenSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="belly_press_belly_off_zeichen"
                )
            if test == "bear_hug_test":
                models.BearHugTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="bear_hug_test")
            if test == "null_grad_aussenrotationstest":
                models.NullGradAußenrotationstestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="null_grad_aussenrotationstest"
                )
            if test == "painful_arc":
                models.PainfulArcSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="painful_arc")
            if test == "hawkins_kennedy_test":
                models.HawkinsKennedyTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="hawkins_kennedy_test"
                )
            if test == "neer_test":
                models.NeerTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="neer_test")
            if test == "unspezifischer_bicepssehenen_test":
                models.UnspezifischerBicepssehenenTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="unspezifischer_bicepssehenen_test"
                )
            if test == "yergason":
                models.YergasonSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="yergason")
            if test == "speedys_test":
                models.SpeedysTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="speedys_test")
            if test == "o_briens_test":
                models.OBriensTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="o_briens_test")
            if test == "biceps_load_test":
                models.BicepsLoadTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="biceps_load_test")
            if test == "supine_flexion_resitance_test":
                models.SupineFlexionResitanceTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(
                    created_for=id, befund="supine_flexion_resitance_test"
                )
            if test == "crank_test":
                models.CrankTestSchulter.objects.create(
                    created_by=request.user, created_for=id
                )
                models.Befund.objects.create(created_for=id, befund="crank_test")

        return redirect(
            "personal_befund", id=id
        )  # Use the name of the URL pattern and pass the id
    befunde = models.Befund.objects.filter(created_for=id)
    befunde_strings = []
    for i in befunde:
        befunde_strings.append(i.befund)
    context = {"already_added": befunde_strings}
    print("jasfkjasfjkasgf")
    print(befunde_strings)
    return render(request, "laxout_app/befund.html", context)


@login_required(login_url="login")
def personal_befund(request, id=None):
    user = models.LaxoutUser.objects.get(id=id)

    # Define your models here
    fragenevaluation_icf_list = models.FragenevaluationNachICFKategorien.objects.filter(
        created_for=id
    )
    fragenevaluation_bio_list = models.FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell.objects.filter(
        created_for=id
    )
    wfragen_list = models.FragenevaluationenNachDen7WFragen.objects.filter(
        created_for=id
    )
    rehaPhase_list = models.StandDerReHaPhase.objects.filter(created_for=id)
    nebenerkrankung_list = models.NebenerkrankungenMedikamente.objects.filter(
        created_for=id
    )
    historia_morbis_list = models.HistoriaMorbis.objects.filter(created_for=id)
    standartbefund_list = models.StandartBefund.objects.filter(created_for=id)
    nrs_numeric_rating_scale_list = models.NrsNumericRatingScale.objects.filter(
        created_for=id
    )
    aktive_beweglichkeit_list = models.AktiveBeweglichkeit.objects.filter(
        created_for=id
    )
    passive_beweglichkeit_list = models.PassiveBeweglichkeit.objects.filter(
        created_for=id
    )
    beweglichkeitsmessung_list = models.BeweglichkeitsmessungKnie.objects.filter(
        created_for=id
    )
    isometrischer_krafttest_list = models.IsometrischerKrafttest.objects.filter(
        created_for=id
    )
    muskelfunktionspruefung_list = models.Muskelfunktionspruefung.objects.filter(
        created_for=id
    )
    einbeinstand60_sekunden_list = models.Einbeinstand60Sekunden.objects.filter(
        created_for=id
    )
    einbeinstand30_sekunden_geschlossene_augen_list = (
        models.Einbeinstand30SekundenGeschlosseneAugen.objects.filter(created_for=id)
    )
    alltagsfunktionen_list = models.Alltagsfunktionen.objects.filter(created_for=id)
    beinlaengenmessung_list = models.Beinlaengenmessung.objects.filter(created_for=id)
    quadriceps_dehnungstest_list = models.QuadricepsDehnungstest.objects.filter(
        created_for=id
    )
    m_rectus_dehnungstest_list = models.MRectusDehnungstest.objects.filter(
        created_for=id
    )
    hamstringtest_list = models.Hamstringtest.objects.filter(created_for=id)
    umfangsmessung_list = models.Umfangsmessung.objects.filter(created_for=id)
    tanzende_patella_list = models.TanzendePatella.objects.filter(created_for=id)
    mini_ergurs_test_list = models.MiniErgussTest.objects.filter(created_for=id)
    glide_test_list = models.GlideTest.objects.filter(created_for=id)
    tilt_test_list = models.TiltTest.objects.filter(created_for=id)
    aprehension_test_list = models.AprehensionTest.objects.filter(created_for=id)
    zohlen_zeichen_list = models.ZohlenZeichen.objects.filter(created_for=id)
    facettendruckschmerztest_list = models.Facettendruckschmerztest.objects.filter(
        created_for=id
    )
    valgus_test_list = models.ValgusTest.objects.filter(created_for=id)
    varus_test_list = models.VarusTest.objects.filter(created_for=id)
    lachmann_test_list = models.LachmannTest.objects.filter(created_for=id)
    vordere_Schublade_list = models.VordereSchublade.objects.filter(created_for=id)
    pivot_shift_test_list = models.PivotShiftTest.objects.filter(created_for=id)
    hintere_schublade_list = models.HintereSchublade.objects.filter(created_for=id)
    gravity_sign_list = models.GravitiySign.objects.filter(created_for=id)
    loomers_test_list = models.LoomersTest.objects.filter(created_for=id)
    steinmann1_list = models.Steinmann1.objects.filter(created_for=id)
    steinmann3_list = models.Steinmann3.objects.filter(created_for=id)
    theslay_test_list = models.TheslayTest.objects.filter(created_for=id)
    mac_murry_test_list = models.MacMurrayTest.objects.filter(created_for=id)
    payr_zeichen_list = models.PayrZeichen.objects.filter(created_for=id)
    apley_zeichen_list = models.ApleyZeichen.objects.filter(created_for=id)
    medio_patellarer_plica_test_list = models.MedioPatellarerPlicaTest.objects.filter(
        created_for=id
    )
    hughston_pica_test_list = models.HughstonPlicaTest.objects.filter(created_for=id)
    red_flag_screening_schulter_list = models.RedFlagScreeningSchulter.objects.filter(
        created_for=id
    )
    aktive_beweglichkeit_schulter_list = (
        models.AktiveBeweglichkeitSchulter.objects.filter(created_for=id)
    )
    passive_beweglichkeit_schulter_list = (
        models.PassiveBeweglichkeitSchulter.objects.filter(created_for=id)
    )
    beweglichkeitsmessung_schulter_list = (
        models.BeweglichkeitsmessungSchulter.objects.filter(created_for=id)
    )
    c_sar_list = models.CopenhagenShoulderAbductionRating.objects.filter(created_for=id)
    posteriore_schultersteifheit_list = (
        models.PosterioreSchultersteifheit.objects.filter(created_for=id)
    )
    isometrischer_krafttest_schulter_list = (
        models.IsometrischerKrafttestSchulter.objects.filter(created_for=id)
    )
    muskelfunktionspruefung_schulter_list = (
        models.MuskelfunktionspruefungSchulter.objects.filter(created_for=id)
    )
    feds_kalassifikation_list = models.FEDSKalassifikationSchulter.objects.filter(
        created_for=id
    )
    anterior_aprehension_test_list = (
        models.AnteriorAprehensionTestSchulter.objects.filter(created_for=id)
    )
    relocation_test_nach_jobe_list = (
        models.RelocationTestnachJobeSchulter.objects.filter(created_for=id)
    )
    surprise_release_test_list = models.SurpriseReleaseTestSchulter.objects.filter(
        created_for=id
    )
    anterior_drawer_test_list = models.AnteriorDrawerTestSchulter.objects.filter(
        created_for=id
    )
    sulcustest_list = models.SulcusTestSchulter.objects.filter(created_for=id)
    posterior_aprehension_test_list = (
        models.PosteriorAprehensionTestSchulter.objects.filter(created_for=id)
    )
    jerk_test_list = models.JerkTestSchulter.objects.filter(created_for=id)
    kim_test_list = models.KimTestSchulter.objects.filter(created_for=id)
    load_and_shift_test_list = models.LoadAndShiftTestSchulter.objects.filter(
        created_for=id
    )
    sulcus_zeichen_list = models.SulcusZeichenSchulter.objects.filter(created_for=id)
    coudance_walch_test_list = models.CoudanceWalchTestSchulter.objects.filter(
        created_for=id
    )
    gargey_test_list = models.GargeyTestSchulter.objects.filter(created_for=id)
    nervenmobilitaetstestungen_bpnt_list = (
        models.NervenmobilitaetstestungenSchulter.objects.filter(created_for=id)
    )
    schnell_anamnese_frozen_shoulder_list = (
        models.SchnellAnamneseFrozenShoulder.objects.filter(created_for=id)
    )
    adsons_test_list = models.AdsonsTestSchulter.objects.filter(created_for=id)
    wrights_test_list = models.WrightsTestHyperabduktionSchulter.objects.filter(
        created_for=id
    )
    edens_test_list = models.EdensTestCostoclavikulaererDruckSchulter.objects.filter(
        created_for=id
    )
    east_test_list = models.ElevatedArmStressTestEASTSchulter.objects.filter(
        created_for=id
    )
    cyrax_release_test_list = models.CyraxReleaseTestSchulter.objects.filter(
        created_for=id
    )
    morley_compression_test_list = models.MorleyCmpressionTestSchulter.objects.filter(
        created_for=id
    )
    irritierbarkeit_schulter_star_list = (
        models.IrritierbarkeitderSchulterAnlehnungSTASchulterDiagnose.objects.filter(
            created_for=id
        )
    )
    alltagsfunktionen_schulter_list = models.AlltagsfunktionenSchulter.objects.filter(
        created_for=id
    )
    umfangsmessung_arm_list = models.UmfangsmessungArm.objects.filter(created_for=id)
    scapula_assistenstest_sat_list = (
        models.ScapulaAssistenstesSATSchulter.objects.filter(created_for=id)
    )
    lateral_scapula_slide_test_list = (
        models.LateralerScapulaSlideTestSchulter.objects.filter(created_for=id)
    )
    scapula_retraction_test_srt_list = (
        models.ScapulaRetractionTestSRTSchulter.objects.filter(created_for=id)
    )
    lateraler_scapula_slide_test_list = (
        models.LateralerScapulaSlideTestSchulter.objects.filter(created_for=id)
    )
    jobe_test_list = models.JobeTestSchulter.objects.filter(created_for=id)
    null_grad_adduktionstest_list = (
        models.NullGradAdduktionstestSchulter.objects.filter(created_for=id)
    )
    drop_arm_zeichen_list = models.DropArmZeichenSchulter.objects.filter(created_for=id)
    lift_off_test_list = models.LiftOffTestSchulter.objects.filter(created_for=id)
    belly_press_belly_off_zeichen_list = (
        models.BellyPressBellyOffZeichenSchulter.objects.filter(created_for=id)
    )
    bear_hug_test_list = models.BearHugTestSchulter.objects.filter(created_for=id)
    null_grad_aussenrotationstest_list = (
        models.NullGradAußenrotationstestSchulter.objects.filter(created_for=id)
    )
    painful_arc_list = models.PainfulArcSchulter.objects.filter(created_for=id)
    hawkins_kennedy_test_list = models.HawkinsKennedyTestSchulter.objects.filter(
        created_for=id
    )
    neer_test_list = models.NeerTestSchulter.objects.filter(created_for=id)
    unspezifischer_bicepssehenen_test_list = (
        models.UnspezifischerBicepssehenenTestSchulter.objects.filter(created_for=id)
    )
    yergason_list = models.YergasonSchulter.objects.filter(created_for=id)
    speedys_test_list = models.SpeedysTestSchulter.objects.filter(created_for=id)
    o_briens_test_list = models.OBriensTestSchulter.objects.filter(created_for=id)
    biceps_load_test_list = models.BicepsLoadTestSchulter.objects.filter(created_for=id)
    supine_flexion_resitance_test_list = (
        models.SupineFlexionResitanceTestSchulter.objects.filter(created_for=id)
    )
    crank_test_list = models.CrankTestSchulter.objects.filter(created_for=id)

    # Initialize context dictionary
    context = {"user": user}

    # Function to add list to context if it exists
    def add_list_to_context(list_obj, context_key):
        if list_obj.exists():
            context[context_key] = list_obj
            ids_list_script = [item.id for item in list_obj]
            context[f"{context_key}_ids"] = ids_list_script

    add_list_to_context(
        red_flag_screening_schulter_list, "red_flag_screening_schulter_list"
    )
    add_list_to_context(
        aktive_beweglichkeit_schulter_list, "aktive_beweglichkeit_schulter_list"
    )
    add_list_to_context(
        passive_beweglichkeit_schulter_list, "passive_beweglichkeit_schulter_list"
    )
    add_list_to_context(
        beweglichkeitsmessung_schulter_list, "beweglichkeitsmessung_schulter_list"
    )
    add_list_to_context(c_sar_list, "c_sar_list")
    add_list_to_context(
        posteriore_schultersteifheit_list, "posteriore_schultersteifheit_list"
    )
    add_list_to_context(
        isometrischer_krafttest_schulter_list, "isometrischer_krafttest_schulter_list"
    )
    add_list_to_context(
        muskelfunktionspruefung_schulter_list, "muskelfunktionspruefung_schulter_list"
    )
    add_list_to_context(feds_kalassifikation_list, "feds_kalassifikation_list")
    add_list_to_context(
        anterior_aprehension_test_list, "anterior_aprehension_test_list"
    )
    add_list_to_context(
        relocation_test_nach_jobe_list, "relocation_test_nach_jobe_list"
    )
    add_list_to_context(surprise_release_test_list, "surprise_release_test_list")
    add_list_to_context(anterior_drawer_test_list, "anterior_drawer_test_list")
    add_list_to_context(sulcustest_list, "sulcustest_list")
    add_list_to_context(
        posterior_aprehension_test_list, "posterior_aprehension_test_list"
    )
    add_list_to_context(jerk_test_list, "jerk_test_list")
    add_list_to_context(kim_test_list, "kim_test_list")
    add_list_to_context(load_and_shift_test_list, "load_and_shift_test_list")
    add_list_to_context(sulcus_zeichen_list, "sulcus_zeichen_list")
    add_list_to_context(coudance_walch_test_list, "coudance_walch_test_list")
    add_list_to_context(gargey_test_list, "gargey_test_list")
    add_list_to_context(
        nervenmobilitaetstestungen_bpnt_list, "nervenmobilitaetstestungen_bpnt_list"
    )
    add_list_to_context(
        schnell_anamnese_frozen_shoulder_list, "schnell_anamnese_frozen_shoulder_list"
    )
    add_list_to_context(adsons_test_list, "adsons_test_list")
    add_list_to_context(wrights_test_list, "wrights_test_list")
    add_list_to_context(edens_test_list, "edens_test_list")
    add_list_to_context(east_test_list, "east_test_list")
    add_list_to_context(cyrax_release_test_list, "cyrax_release_test_list")
    add_list_to_context(morley_compression_test_list, "morley_compression_test_list")
    add_list_to_context(
        irritierbarkeit_schulter_star_list, "irritierbarkeit_schulter_star_list"
    )
    add_list_to_context(
        alltagsfunktionen_schulter_list, "alltagsfunktionen_schulter_list"
    )
    add_list_to_context(umfangsmessung_arm_list, "umfangsmessung_arm_list")
    add_list_to_context(
        scapula_assistenstest_sat_list, "scapula_assistenstest_sat_list"
    )
    add_list_to_context(
        lateral_scapula_slide_test_list, "lateral_scapula_slide_test_list"
    )
    add_list_to_context(
        scapula_retraction_test_srt_list, "scapula_retraction_test_srt_list"
    )
    add_list_to_context(
        lateraler_scapula_slide_test_list, "lateraler_scapula_slide_test_list"
    )
    add_list_to_context(jobe_test_list, "jobe_test_list")
    add_list_to_context(null_grad_adduktionstest_list, "null_grad_adduktionstest_list")
    add_list_to_context(drop_arm_zeichen_list, "drop_arm_zeichen_list")
    add_list_to_context(lift_off_test_list, "lift_off_test_list")
    add_list_to_context(
        belly_press_belly_off_zeichen_list, "belly_press_belly_off_zeichen_list"
    )
    add_list_to_context(bear_hug_test_list, "bear_hug_test_list")
    add_list_to_context(
        null_grad_aussenrotationstest_list, "null_grad_aussenrotationstest_list"
    )
    add_list_to_context(painful_arc_list, "painful_arc_list")
    add_list_to_context(hawkins_kennedy_test_list, "hawkins_kennedy_test_list")
    add_list_to_context(neer_test_list, "neer_test_list")
    add_list_to_context(
        unspezifischer_bicepssehenen_test_list, "unspezifischer_bicepssehenen_test_list"
    )
    add_list_to_context(yergason_list, "yergason_list")
    add_list_to_context(speedys_test_list, "speedys_test_list")
    add_list_to_context(o_briens_test_list, "o_briens_test_list")
    add_list_to_context(biceps_load_test_list, "biceps_load_test_list")
    add_list_to_context(
        supine_flexion_resitance_test_list, "supine_flexion_resitance_test_list"
    )
    add_list_to_context(crank_test_list, "crank_test_list")

    # Add lists to context using the function
    add_list_to_context(standartbefund_list, "standartbefund_list")
    add_list_to_context(nrs_numeric_rating_scale_list, "nrs_numeric_rating_scale_list")
    add_list_to_context(aktive_beweglichkeit_list, "aktive_beweglichkeit_list")
    add_list_to_context(passive_beweglichkeit_list, "passive_beweglichkeit_list")
    add_list_to_context(beweglichkeitsmessung_list, "beweglichkeitsmessung_list")
    add_list_to_context(isometrischer_krafttest_list, "isometrischer_krafttest_list")
    add_list_to_context(muskelfunktionspruefung_list, "muskelfunktionspruefung_list")
    add_list_to_context(einbeinstand60_sekunden_list, "einbeinstand60_sekunden_list")
    add_list_to_context(
        einbeinstand30_sekunden_geschlossene_augen_list,
        "einbeinstand30_sekunden_geschlossene_augen_list",
    )
    add_list_to_context(alltagsfunktionen_list, "alltagsfunktionen_list")
    add_list_to_context(beinlaengenmessung_list, "beinlaengenmessung_list")
    add_list_to_context(quadriceps_dehnungstest_list, "quadriceps_dehnungstest_list")
    add_list_to_context(m_rectus_dehnungstest_list, "m_rectus_dehnungstest_list")
    add_list_to_context(hamstringtest_list, "hamstringtest_list")
    add_list_to_context(umfangsmessung_list, "umfangsmessung_list")
    add_list_to_context(tanzende_patella_list, "tanzende_patella_list")
    add_list_to_context(mini_ergurs_test_list, "mini_ergurs_test_list")
    add_list_to_context(glide_test_list, "glide_test_list")
    add_list_to_context(tilt_test_list, "tilt_test_list")
    add_list_to_context(aprehension_test_list, "aprehension_test_list")
    add_list_to_context(zohlen_zeichen_list, "zohlen_zeichen_list")
    add_list_to_context(facettendruckschmerztest_list, "facettendruckschmerztest_list")
    add_list_to_context(valgus_test_list, "valgus_test_list")
    add_list_to_context(varus_test_list, "varus_test_list")
    add_list_to_context(lachmann_test_list, "lachmann_test_list")
    add_list_to_context(vordere_Schublade_list, "vordere_Schublade_list")
    add_list_to_context(pivot_shift_test_list, "pivot_shift_test_list")
    add_list_to_context(hintere_schublade_list, "hintere_schublade_list")
    add_list_to_context(gravity_sign_list, "gravity_sign_list")
    add_list_to_context(loomers_test_list, "loomers_test_list")
    add_list_to_context(steinmann1_list, "steinmann1_list")
    add_list_to_context(steinmann3_list, "steinmann3_list")
    add_list_to_context(theslay_test_list, "theslay_test_list")
    add_list_to_context(mac_murry_test_list, "mac_murry_test_list")
    add_list_to_context(payr_zeichen_list, "payr_zeichen_list")
    add_list_to_context(apley_zeichen_list, "apley_zeichen_list")
    add_list_to_context(
        medio_patellarer_plica_test_list, "medio_patellarer_plica_test_list"
    )
    add_list_to_context(hughston_pica_test_list, "hughston_pica_test_list")
    add_list_to_context(fragenevaluation_bio_list, "fragenevaluation_bio_list")
    add_list_to_context(fragenevaluation_icf_list, "fragenevaluation_icf_list")
    add_list_to_context(wfragen_list, "wfragen_list")
    add_list_to_context(rehaPhase_list, "rehaPhase_list")
    add_list_to_context(nebenerkrankung_list, "nebenerkrankung_list")
    add_list_to_context(historia_morbis_list, "historia_morbis_list")

    model_fields = models.RedFlagScreeningSchulter._meta.get_fields()
    extracted_fields = ["created_for", "created_by", "id", "created_at"]
    model_names_csar = [field.name for field in model_fields if field.name not in extracted_fields]

    print(model_names_csar)

    ## Test mit listen der argumente für java Script

    print(context)

    return render(request, "laxout_app/personal_befund.html", context)


@login_required(login_url="login")
def update_personal_befund(request, id=None, befund=None, befundId=None):
    if id == None:
        return HttpResponse("Not valid")
    excluded_fields = ["created_at", "created_by", "created_for", "id"]
    if befund == "ananmese":
        selected_befund = models.AnanmenseBefund.objects.get(id=befundId)
        disability = request.POST.get("disability")
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        selected_befund.disability = disability
        selected_befund.name = name
        selected_befund.surname = surname
        selected_befund.save()

    if befund == "fragenevaluation_icf":
        selected_befund = models.FragenevaluationNachICFKategorien.objects.get(
            id=befundId
        )
        # op = request.POST.get("op")
        # if op == "1":
        #     op = True
        #     print("TRUE")
        # else:
        #     op = False
        #     aktueller_gesundheitszustand = models.CharField(default="", max_length=20000)
        # struktur_funktion = models.CharField(default="", max_length=20000)
        # aktivitaet = models.CharField(default="", max_length=20000)
        # partizipation = models.CharField(default="", max_length=20000)
        # kontextfaktoren = models.CharField(default="", max_length=20000)
        aktueller_gesundheitszustand = request.POST.get("aktueller_gesundheitszustand")
        struktur_funktion = request.POST.get("struktur_funktion")
        aktivitaet = request.POST.get("aktivitaet")
        partizipation = request.POST.get("partizipation")
        kontextfaktoren = request.POST.get("kontextfaktoren")

        selected_befund.aktueller_gesundheitszustand = aktueller_gesundheitszustand
        selected_befund.struktur_funktion = struktur_funktion
        selected_befund.aktivitaet = aktivitaet
        selected_befund.partizipation = partizipation
        selected_befund.kontextfaktoren = kontextfaktoren

        selected_befund.save()

    if befund == "fragenevaluation_bio_psycho_sozial_krankheitsmodell":
        selected_befund = models.FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell.objects.get(
            id=befundId
        )

        koerperliche_beschwerden = request.POST.get("koerperliche_beschwerden")
        psychisch_gelagerte_eschwerden = request.POST.get(
            "psychisch_gelagerte_eschwerden"
        )
        probleme_mit_aktiver_teilhabe_am_sozialen_Leben = request.POST.get(
            "probleme_mit_aktiver_teilhabe_am_sozialen_Leben"
        )

        selected_befund.koerperliche_beschwerden = koerperliche_beschwerden
        selected_befund.psychisch_gelagerte_eschwerden = psychisch_gelagerte_eschwerden
        selected_befund.probleme_mit_aktiver_teilhabe_am_sozialen_Leben = (
            probleme_mit_aktiver_teilhabe_am_sozialen_Leben
        )

        selected_befund.save()

    if befund == "w_fragen":
        selected_befund = models.FragenevaluationenNachDen7WFragen.objects.get(
            id=befundId
        )

        hauptbeschwerden = request.POST.get("hauptbeschwerden")
        lokalisierung = request.POST.get("lokalisierung")
        provokation = request.POST.get("provokation")
        orientierung_für_Maßnahmen = request.POST.get("orientierung_für_Maßnahmen")
        schmerzqualität = request.POST.get("schmerzqualität")
        orientierung = request.POST.get("orientierung")
        beschwerdeverlauf = request.POST.get("beschwerdeverlauf")

        selected_befund.beschwerdeverlauf = beschwerdeverlauf
        selected_befund.orientierung = orientierung
        selected_befund.schmerzqualität = schmerzqualität
        selected_befund.orientierung_für_Maßnahmen = orientierung_für_Maßnahmen
        selected_befund.provokation = provokation
        selected_befund.lokalisierung = lokalisierung
        selected_befund.hauptbeschwerden = hauptbeschwerden

        selected_befund.save()

    if befund == "standart_befund":
        selected_befund = models.StandartBefund.objects.get(id=befundId)

        dropdown_aktualisierung = request.POST.get("dropdown")
        if dropdown_aktualisierung:
            geschlecht = request.POST.get("geschlecht")
            selected_befund.geschlecht = geschlecht
            selected_befund.save()
            return HttpResponse("Updated Successfully")

        # Felder einzeln aktualisieren, falls sie im POST-Request vorhanden sind
        if "name" in request.POST:
            selected_befund.name = request.POST.get("name")
        if "vorname" in request.POST:
            selected_befund.vorname = request.POST.get("vorname")
        if "alter" in request.POST:
            selected_befund.alter = request.POST.get("alter")
        if "diagnose" in request.POST:
            selected_befund.diagnose = request.POST.get("diagnose")
        if "hauptziel" in request.POST:
            selected_befund.hauptziel = request.POST.get("hauptziel")
        if "vollbelastung" in request.POST:
            selected_befund.vollbelastung = request.POST.get("vollbelastung")
        if "teilbeslastung" in request.POST:
            selected_befund.teilbeslastung = request.POST.get("teilbeslastung")
        if "lagerungstabil" in request.POST:
            selected_befund.lagerungstabil = request.POST.get("lagerungstabil")
        if "maximalpuls" in request.POST:
            selected_befund.maximalpuls = request.POST.get("maximalpuls")
        if "therapeutische_ziele_maßnahmen" in request.POST:
            selected_befund.therapeutische_ziele_maßnahmen = request.POST.get(
                "therapeutische_ziele_maßnahmen"
            )
        if "medikament_einnahme" in request.POST:
            selected_befund.medikament_einnahme = request.POST.get(
                "medikament_einnahme"
            )
        if "groeße" in request.POST:
            selected_befund.groeße = request.POST.get("groeße")
        if "gewicht" in request.POST:
            selected_befund.gewicht = request.POST.get("gewicht")
        if "konstitutionstyp" in request.POST:
            selected_befund.konstitutionstyp = request.POST.get("konstitutionstyp")
        if "beruf" in request.POST:
            selected_befund.beruf = request.POST.get("beruf")
        if "alltagsaktivitaeten" in request.POST:
            selected_befund.alltagsaktivitaeten = request.POST.get(
                "alltagsaktivitaeten"
            )
        if "op_vorliegend" in request.POST:
            selected_befund.op_vorliegend = request.POST.get("op_vorliegend")

        selected_befund.save()

    if befund == "stand_reha_phase":
        selected_befund = models.StandDerReHaPhase.objects.get(id=befundId)

        akute_phase = request.POST.get("akute_phase")
        wundheilungsphase = request.POST.get("wundheilungsphase")
        frueh_phase_ReHa = request.POST.get("frueh_phase_ReHa")
        mittlere_phase_Reha = request.POST.get("mittlere_phase_Reha")
        spaet_phase_reha = request.POST.get("spaet_phase_reha")

        selected_befund.akute_phase = akute_phase
        selected_befund.wundheilungsphase = wundheilungsphase
        selected_befund.frueh_phase_ReHa = frueh_phase_ReHa
        selected_befund.mittlere_phase_Reha = mittlere_phase_Reha
        selected_befund.spaet_phase_reha = spaet_phase_reha

        selected_befund.save()

    if befund == "nebenerkrankungen_medikamente":
        selected_befund = models.NebenerkrankungenMedikamente.objects.get(id=befundId)

        erbkrankheiten = request.POST.get("erbkrankheiten")
        metabolische_erkrankungen = request.POST.get("metabolische_erkrankungen")
        psychische_erkrankungen = request.POST.get("psychische_erkrankungen")
        herz_kreislauferkrankungen = request.POST.get("herz_kreislauferkrankungen")
        neurologische_erkrankungen = request.POST.get("neurologische_erkrankungen")
        rheumatisch_entzuendliche_erkrankungen = request.POST.get(
            "rheumatisch_entzuendliche_erkrankungen"
        )
        erkrankungen_bewegungsapparat = request.POST.get(
            "erkrankungen_bewegungsapparat"
        )
        erbkrankheiten_krankheit = request.POST.get("erbkrankheiten_krankheit")
        metabolische_erkrankungen_krankheit = request.POST.get(
            "metabolische_erkrankungen_krankheit"
        )
        psychische_erkrankungen_krankheit = request.POST.get(
            "psychische_erkrankungen_krankheit"
        )
        herz_kreislauferkrankungen_krankheit = request.POST.get(
            "herz_kreislauferkrankungen_krankheit"
        )
        neurologische_erkrankungen_krankheit = request.POST.get(
            "neurologische_erkrankungen_krankheit"
        )
        rheumatisch_entzuendliche_erkrankungen_krankheit = request.POST.get(
            "rheumatisch_entzuendliche_erkrankungen"
        )
        erkrankungen_bewegungsapparat_erkrankungen_krankheit = request.POST.get(
            "erkrankungen_bewegungsapparat_erkrankungen_krankheit"
        )
        erbkrankheiten_medikamente = request.POST.get("erbkrankheiten_medikamente")
        metabolische_erkrankungen_medikamente = request.POST.get(
            "metabolische_erkrankungen_medikamente"
        )
        psychische_erkrankungen_medikamente = request.POST.get(
            "psychische_erkrankungen_medikamente"
        )
        herz_kreislauferkrankungen_medikamente = request.POST.get(
            "herz_kreislauferkrankungen_medikamente"
        )
        neurologische_erkrankungen_medikamente = request.POST.get(
            "neurologische_erkrankungen_medikamente"
        )
        rheumatisch_entzuendliche_erkrankungen_medikamente = request.POST.get(
            "rheumatisch_entzuendliche_erkrankungen_medikamente"
        )
        erkrankungen_bewegungsapparat_erkrankungen_medikamente = request.POST.get(
            "erkrankungen_bewegungsapparat_erkrankungen_medikamente"
        )

        selected_befund.erbkrankheiten = erbkrankheiten
        selected_befund.metabolische_erkrankungen = metabolische_erkrankungen
        selected_befund.psychische_erkrankungen = psychische_erkrankungen
        selected_befund.herz_kreislauferkrankungen = herz_kreislauferkrankungen
        selected_befund.neurologische_erkrankungen = neurologische_erkrankungen
        selected_befund.rheumatisch_entzuendliche_erkrankungen = (
            rheumatisch_entzuendliche_erkrankungen
        )
        selected_befund.erkrankungen_bewegungsapparat = erkrankungen_bewegungsapparat

        selected_befund.erbkrankheiten_krankheit = erbkrankheiten_krankheit
        selected_befund.metabolische_erkrankungen_krankheit = (
            metabolische_erkrankungen_krankheit
        )
        selected_befund.psychische_erkrankungen_krankheit = (
            psychische_erkrankungen_krankheit
        )
        selected_befund.herz_kreislauferkrankungen_krankheit = (
            herz_kreislauferkrankungen_krankheit
        )
        selected_befund.neurologische_erkrankungen_krankheit = (
            neurologische_erkrankungen_krankheit
        )
        selected_befund.rheumatisch_entzuendliche_erkrankungen_krankheit = (
            rheumatisch_entzuendliche_erkrankungen_krankheit
        )
        selected_befund.erkrankungen_bewegungsapparat_erkrankungen_krankheit = (
            erkrankungen_bewegungsapparat_erkrankungen_krankheit
        )

        selected_befund.erbkrankheiten_medikamente = erbkrankheiten_medikamente
        selected_befund.metabolische_erkrankungen_medikamente = (
            metabolische_erkrankungen_medikamente
        )
        selected_befund.psychische_erkrankungen_medikamente = (
            psychische_erkrankungen_medikamente
        )
        selected_befund.herz_kreislauferkrankungen_medikamente = (
            herz_kreislauferkrankungen_medikamente
        )
        selected_befund.neurologische_erkrankungen_medikamente = (
            neurologische_erkrankungen_medikamente
        )
        selected_befund.rheumatisch_entzuendliche_erkrankungen_medikamente = (
            rheumatisch_entzuendliche_erkrankungen_medikamente
        )
        selected_befund.erkrankungen_bewegungsapparat_erkrankungen_medikamente = (
            erkrankungen_bewegungsapparat_erkrankungen_medikamente
        )

        selected_befund.save()

    if befund == "historia_morbis":
        selected_befund = models.HistoriaMorbis.objects.get(id=befundId)

        trauma_unfall = request.POST.get("trauma_unfall")
        atraumatisch = request.POST.get("atraumatisch")
        chronisch = request.POST.get("chronisch")
        progredient = request.POST.get("progredient")
        krankheitsverlauf = request.POST.get("krankheitsverlauf")
        Krankenhausaufenthalte = request.POST.get("Krankenhausaufenthalte")
        unfaelle_verletzungen_operationen = request.POST.get(
            "unfaelle_verletzungen_operationen"
        )
        schwangerschaften = request.POST.get("schwangerschaften")
        sucht_drogenverhalten = request.POST.get("sucht_drogenverhalten")

        selected_befund.trauma_unfall = trauma_unfall
        selected_befund.atraumatisch = atraumatisch
        selected_befund.chronisch = chronisch
        selected_befund.progredient = progredient
        selected_befund.krankheitsverlauf = krankheitsverlauf
        selected_befund.Krankenhausaufenthalte = Krankenhausaufenthalte
        selected_befund.unfaelle_verletzungen_operationen = (
            unfaelle_verletzungen_operationen
        )
        selected_befund.schwangerschaften = schwangerschaften
        selected_befund.sucht_drogenverhalten = sucht_drogenverhalten

        selected_befund.save()

    if befund == "nrs_numeric_rating_scale":
        selected_befund = models.NrsNumericRatingScale.objects.get(id=befundId)

        if "kein_schmerz" in request.POST:
            selected_befund.kein_schmerz = request.POST.get("kein_schmerz")

        if "sanft" in request.POST:
            selected_befund.sanft = request.POST.get("sanft")

        if "gering" in request.POST:
            selected_befund.gering = request.POST.get("gering")

        if "unbequem" in request.POST:
            selected_befund.unbequem = request.POST.get("unbequem")

        if "mittelgradig" in request.POST:
            selected_befund.mittelgradig = request.POST.get("mittelgradig")

        if "ablenkend" in request.POST:
            selected_befund.ablenkend = request.POST.get("ablenkend")

        if "quaelend" in request.POST:
            selected_befund.quaelend = request.POST.get("quaelend")

        if "starker_schmerz" in request.POST:
            selected_befund.starker_schmerz = request.POST.get("starker_schmerz")

        if "hochgradiger_schmerz" in request.POST:
            selected_befund.hochgradiger_schmerz = request.POST.get(
                "hochgradiger_schmerz"
            )

        if "unertraeglich" in request.POST:
            selected_befund.unertraeglich = request.POST.get("unertraeglich")

        if "unbeschreiblich" in request.POST:
            selected_befund.unbeschreiblich = request.POST.get("unbeschreiblich")

        selected_befund.save()

    if befund == "aktive_beweglichkeit":
        selected_befund = models.AktiveBeweglichkeit.objects.get(id=befundId)

        # Flexion Rechts
        if "flexion_rechts_oB" in request.POST:
            selected_befund.flexion_rechts_oB = request.POST.get("flexion_rechts_oB")
        if "flexion_rechts_leicht_begrenzt" in request.POST:
            selected_befund.flexion_rechts_leicht_begrenzt = request.POST.get(
                "flexion_rechts_leicht_begrenzt"
            )
        if "flexion_rechts_mittelgradig_begrenzt" in request.POST:
            selected_befund.flexion_rechts_mittelgradig_begrenzt = request.POST.get(
                "flexion_rechts_mittelgradig_begrenzt"
            )
        if "flexion_rechts_stark_begrenzt" in request.POST:
            selected_befund.flexion_rechts_stark_begrenzt = request.POST.get(
                "flexion_rechts_stark_begrenzt"
            )
        if "flexion_rechts_schmerzhaft" in request.POST:
            selected_befund.flexion_rechts_schmerzhaft = request.POST.get(
                "flexion_rechts_schmerzhaft"
            )
        if "flexion_rechts_gehemmt" in request.POST:
            selected_befund.flexion_rechts_gehemmt = request.POST.get(
                "flexion_rechts_gehemmt"
            )
        if "flexion_rechts_verzögert" in request.POST:
            selected_befund.flexion_rechts_verzögert = request.POST.get(
                "flexion_rechts_verzögert"
            )
        if "flexion_rechts_eingeschränkt" in request.POST:
            selected_befund.flexion_rechts_eingeschränkt = request.POST.get(
                "flexion_rechts_eingeschränkt"
            )
        if "flexion_rechts_unkoordiniert" in request.POST:
            selected_befund.flexion_rechts_unkoordiniert = request.POST.get(
                "flexion_rechts_unkoordiniert"
            )

        # Flexion Links
        if "flexion_links_oB" in request.POST:
            selected_befund.flexion_links_oB = request.POST.get("flexion_links_oB")
        if "flexion_links_leicht_begrenzt" in request.POST:
            selected_befund.flexion_links_leicht_begrenzt = request.POST.get(
                "flexion_links_leicht_begrenzt"
            )
        if "flexion_links_mittelgradig_begrenzt" in request.POST:
            selected_befund.flexion_links_mittelgradig_begrenzt = request.POST.get(
                "flexion_links_mittelgradig_begrenzt"
            )
        if "flexion_links_stark_begrenzt" in request.POST:
            selected_befund.flexion_links_stark_begrenzt = request.POST.get(
                "flexion_links_stark_begrenzt"
            )
        if "flexion_links_schmerzhaft" in request.POST:
            selected_befund.flexion_links_schmerzhaft = request.POST.get(
                "flexion_links_schmerzhaft"
            )
        if "flexion_links_gehemmt" in request.POST:
            selected_befund.flexion_links_gehemmt = request.POST.get(
                "flexion_links_gehemmt"
            )
        if "flexion_links_verzögert" in request.POST:
            selected_befund.flexion_links_verzögert = request.POST.get(
                "flexion_links_verzögert"
            )
        if "flexion_links_eingeschränkt" in request.POST:
            selected_befund.flexion_links_eingeschränkt = request.POST.get(
                "flexion_links_eingeschränkt"
            )
        if "flexion_links_unkoordiniert" in request.POST:
            selected_befund.flexion_links_unkoordiniert = request.POST.get(
                "flexion_links_unkoordiniert"
            )

        # Extension Rechts
        if "extension_rechts_oB" in request.POST:
            selected_befund.extension_rechts_oB = request.POST.get(
                "extension_rechts_oB"
            )
        if "extension_rechts_leicht_begrenzt" in request.POST:
            selected_befund.extension_rechts_leicht_begrenzt = request.POST.get(
                "extension_rechts_leicht_begrenzt"
            )
        if "extension_rechts_mittelgradig_begrenzt" in request.POST:
            selected_befund.extension_rechts_mittelgradig_begrenzt = request.POST.get(
                "extension_rechts_mittelgradig_begrenzt"
            )
        if "extension_rechts_stark_begrenzt" in request.POST:
            selected_befund.extension_rechts_stark_begrenzt = request.POST.get(
                "extension_rechts_stark_begrenzt"
            )
        if "extension_rechts_schmerzhaft" in request.POST:
            selected_befund.extension_rechts_schmerzhaft = request.POST.get(
                "extension_rechts_schmerzhaft"
            )
        if "extension_rechts_gehemmt" in request.POST:
            selected_befund.extension_rechts_gehemmt = request.POST.get(
                "extension_rechts_gehemmt"
            )
        if "extension_rechts_verzögert" in request.POST:
            selected_befund.extension_rechts_verzögert = request.POST.get(
                "extension_rechts_verzögert"
            )
        if "extension_rechts_eingeschränkt" in request.POST:
            selected_befund.extension_rechts_eingeschränkt = request.POST.get(
                "extension_rechts_eingeschränkt"
            )
        if "extension_rechts_unkoordiniert" in request.POST:
            selected_befund.extension_rechts_unkoordiniert = request.POST.get(
                "extension_rechts_unkoordiniert"
            )

        # Extension Links
        if "extension_links_oB" in request.POST:
            selected_befund.extension_links_oB = request.POST.get("extension_links_oB")
        if "extension_links_leicht_begrenzt" in request.POST:
            selected_befund.extension_links_leicht_begrenzt = request.POST.get(
                "extension_links_leicht_begrenzt"
            )
        if "extension_links_mittelgradig_begrenzt" in request.POST:
            selected_befund.extension_links_mittelgradig_begrenzt = request.POST.get(
                "extension_links_mittelgradig_begrenzt"
            )
        if "extension_links_stark_begrenzt" in request.POST:
            selected_befund.extension_links_stark_begrenzt = request.POST.get(
                "extension_links_stark_begrenzt"
            )
        if "extension_links_schmerzhaft" in request.POST:
            selected_befund.extension_links_schmerzhaft = request.POST.get(
                "extension_links_schmerzhaft"
            )
        if "extension_links_gehemmt" in request.POST:
            selected_befund.extension_links_gehemmt = request.POST.get(
                "extension_links_gehemmt"
            )
        if "extension_links_verzögert" in request.POST:
            selected_befund.extension_links_verzögert = request.POST.get(
                "extension_links_verzögert"
            )
        if "extension_links_eingeschränkt" in request.POST:
            selected_befund.extension_links_eingeschränkt = request.POST.get(
                "extension_links_eingeschränkt"
            )
        if "extension_links_unkoordiniert" in request.POST:
            selected_befund.extension_links_unkoordiniert = request.POST.get(
                "extension_links_unkoordiniert"
            )

        selected_befund.save()

    if befund == "passive_beweglichkeit":
        selected_befund = models.PassiveBeweglichkeit.objects.get(id=befundId)

        # Flexion Rechts
        if "flexion_rechts_oB_pb" in request.POST:

            selected_befund.flexion_rechts_oB = request.POST.get("flexion_rechts_oB_pb")
        if "flexion_rechts_leicht_begrenzt_pb" in request.POST:
            selected_befund.flexion_rechts_leicht_begrenzt = request.POST.get(
                "flexion_rechts_leicht_begrenzt_pb"
            )
        if "flexion_rechts_mittelgradig_begrenzt_pb" in request.POST:
            selected_befund.flexion_rechts_mittelgradig_begrenzt = request.POST.get(
                "flexion_rechts_mittelgradig_begrenzt_pb"
            )
        if "flexion_rechts_stark_begrenzt_pb" in request.POST:
            selected_befund.flexion_rechts_stark_begrenzt = request.POST.get(
                "flexion_rechts_stark_begrenzt_pb"
            )
        if "flexion_rechts_fest_elastischer_stopp" in request.POST:
            selected_befund.flexion_rechts_fest_elastischer_stopp = request.POST.get(
                "flexion_rechts_fest_elastischer_stopp"
            )
        if "flexion_rechts_weich_elastischer_stopp" in request.POST:
            selected_befund.flexion_rechts_weich_elastischer_stopp = request.POST.get(
                "flexion_rechts_weich_elastischer_stopp"
            )
        if "flexion_rechts_hart_unelastischer_stopp" in request.POST:
            selected_befund.flexion_rechts_hart_unelastischer_stopp = request.POST.get(
                "flexion_rechts_hart_unelastischer_stopp"
            )
        if "flexion_rechts_fester_unelastischer_stopp" in request.POST:
            selected_befund.flexion_rechts_fester_unelastischer_stopp = (
                request.POST.get("flexion_rechts_fester_unelastischer_stopp")
            )
        if "flexion_rechts_fester_elastischer_stopp" in request.POST:
            selected_befund.flexion_rechts_fester_elastischer_stopp = request.POST.get(
                "flexion_rechts_fester_elastischer_stopp"
            )
        if "flexion_rechts_leeres_endgefuehl" in request.POST:
            selected_befund.flexion_rechts_leeres_endgefuehl = request.POST.get(
                "flexion_rechts_leeres_endgefuehl"
            )
        if "flexion_rechts_schmerz" in request.POST:
            selected_befund.flexion_rechts_schmerz = request.POST.get(
                "flexion_rechts_schmerz"
            )

        # Flexion Links
        if "flexion_links_oB_pb" in request.POST:
            selected_befund.flexion_links_oB = request.POST.get("flexion_links_oB_pb")
        if "flexion_links_leicht_begrenzt_pb" in request.POST:
            selected_befund.flexion_links_leicht_begrenzt = request.POST.get(
                "flexion_links_leicht_begrenzt_pb"
            )
        if "flexion_links_mittelgradig_begrenzt_pb" in request.POST:
            selected_befund.flexion_links_mittelgradig_begrenzt = request.POST.get(
                "flexion_links_mittelgradig_begrenzt_pb"
            )
        if "flexion_links_stark_begrenzt_pb" in request.POST:
            selected_befund.flexion_links_stark_begrenzt = request.POST.get(
                "flexion_links_stark_begrenzt_pb"
            )
        if "flexion_links_fest_elastischer_stopp" in request.POST:
            selected_befund.flexion_links_fest_elastischer_stopp = request.POST.get(
                "flexion_links_fest_elastischer_stopp"
            )
        if "flexion_links_weich_elastischer_stopp" in request.POST:
            selected_befund.flexion_links_weich_elastischer_stopp = request.POST.get(
                "flexion_links_weich_elastischer_stopp"
            )
        if "flexion_links_hart_unelastischer_stopp" in request.POST:
            selected_befund.flexion_links_hart_unelastischer_stopp = request.POST.get(
                "flexion_links_hart_unelastischer_stopp"
            )
        if "flexion_links_fester_unelastischer_stopp" in request.POST:
            selected_befund.flexion_links_fester_unelastischer_stopp = request.POST.get(
                "flexion_links_fester_unelastischer_stopp"
            )
        if "flexion_links_fester_elastischer_stopp" in request.POST:
            selected_befund.flexion_links_fester_elastischer_stopp = request.POST.get(
                "flexion_links_fester_elastischer_stopp"
            )
        if "flexion_links_leeres_endgefuehl" in request.POST:
            selected_befund.flexion_links_leeres_endgefuehl = request.POST.get(
                "flexion_links_leeres_endgefuehl"
            )
        if "flexion_links_schmerz" in request.POST:
            selected_befund.flexion_links_schmerz = request.POST.get(
                "flexion_links_schmerz"
            )

        # Extension Rechts
        if "extension_rechts_oB_pb" in request.POST:
            selected_befund.extension_rechts_oB = request.POST.get(
                "extension_rechts_oB_pb"
            )
        if "extension_rechts_leicht_begrenzt_pb" in request.POST:
            selected_befund.extension_rechts_leicht_begrenzt = request.POST.get(
                "extension_rechts_leicht_begrenzt_pb"
            )
        if "extension_rechts_mittelgradig_begrenzt_pb" in request.POST:
            print("AUFGERUFEN")
            print(request.POST.get("extension_rechts_mittelgradig_begrenzt_pb"))
            selected_befund.extension_rechts_mittelgradig_begrenztb = request.POST.get(
                "extension_rechts_mittelgradig_begrenzt_pb"
            )
        if "extension_rechts_stark_begrenzt_pb" in request.POST:
            selected_befund.extension_rechts_stark_begrenzt = request.POST.get(
                "extension_rechts_stark_begrenzt_pb"
            )
        if "extension_rechts_fest_elastischer_stopp" in request.POST:
            selected_befund.extension_rechts_fest_elastischer_stopp = request.POST.get(
                "extension_rechts_fest_elastischer_stopp"
            )
        if "extension_rechts_weich_elastischer_stopp" in request.POST:
            selected_befund.extension_rechts_weich_elastischer_stopp = request.POST.get(
                "extension_rechts_weich_elastischer_stopp"
            )
        if "extension_rechts_hart_unelastischer_stopp" in request.POST:
            selected_befund.extension_rechts_hart_unelastischer_stopp = (
                request.POST.get("extension_rechts_hart_unelastischer_stopp")
            )
        if "extension_rechts_fester_unelastischer_stopp" in request.POST:
            selected_befund.extension_rechts_fester_unelastischer_stopp = (
                request.POST.get("extension_rechts_fester_unelastischer_stopp")
            )
        if "extension_rechts_fester_elastischer_stopp" in request.POST:
            selected_befund.extension_rechts_fester_elastischer_stopp = (
                request.POST.get("extension_rechts_fester_elastischer_stopp")
            )
        if "extension_rechts_leeres_endgefuehl" in request.POST:
            selected_befund.extension_rechts_leeres_endgefuehl = request.POST.get(
                "extension_rechts_leeres_endgefuehl"
            )
        if "extension_rechts_schmerz" in request.POST:
            selected_befund.extension_rechts_schmerz = request.POST.get(
                "extension_rechts_schmerz"
            )

        # Extension Links
        if "extension_links_oB_pb" in request.POST:
            selected_befund.extension_links_oB = request.POST.get(
                "extension_links_oB_pb"
            )

        if "extension_links_leicht_begrenzt_pb" in request.POST:
            selected_befund.extension_links_leicht_begrenzt = request.POST.get(
                "extension_links_leicht_begrenzt_pb"
            )
        if "extension_links_mittelgradig_begrenzt_pb" in request.POST:
            selected_befund.extension_links_mittelgradig_begrenzt = request.POST.get(
                "extension_links_mittelgradig_begrenzt_pb"
            )
        if "extension_links_stark_begrenzt_pb" in request.POST:
            selected_befund.extension_links_stark_begrenzt = request.POST.get(
                "extension_links_stark_begrenzt_pb"
            )
        if "extension_links_fest_elastischer_stopp" in request.POST:
            selected_befund.extension_links_fest_elastischer_stopp = request.POST.get(
                "extension_links_fest_elastischer_stopp"
            )
        if "extension_links_weich_elastischer_stopp" in request.POST:
            selected_befund.extension_links_weich_elastischer_stopp = request.POST.get(
                "extension_links_weich_elastischer_stopp"
            )
        if "extension_links_hart_unelastischer_stopp" in request.POST:
            selected_befund.extension_links_hart_unelastischer_stopp = request.POST.get(
                "extension_links_hart_unelastischer_stopp"
            )
        if "extension_links_fester_unelastischer_stopp" in request.POST:
            selected_befund.extension_links_fester_unelastischer_stopp = (
                request.POST.get("extension_links_fester_unelastischer_stopp")
            )
        if "extension_links_fester_elastischer_stopp" in request.POST:
            selected_befund.extension_links_fester_elastischer_stopp = request.POST.get(
                "extension_links_fester_elastischer_stopp"
            )
        if "extension_links_leeres_endgefuehl" in request.POST:
            selected_befund.extension_links_leeres_endgefuehl = request.POST.get(
                "extension_links_leeres_endgefuehl"
            )
        if "extension_links_schmerz" in request.POST:
            selected_befund.extension_links_schmerz = request.POST.get(
                "extension_links_schmerz"
            )

        selected_befund.save()

    if befund == "beweglichkeitsmessung":
        selected_befund = models.BeweglichkeitsmessungKnie.objects.get(id=befundId)

        if "extension_flexion_rechts_value_bmk" in request.POST:
            selected_befund.extension_flexion_rechts_value = request.POST.get(
                "extension_flexion_rechts_value_bmk"
            )
        if "extension_flexion_links_value_bmk" in request.POST:
            selected_befund.extension_flexion_links_value = request.POST.get(
                "extension_flexion_links_value_bmk"
            )

        selected_befund.save()

    if befund == "isometrischer_krafttest":
        selected_befund = models.IsometrischerKrafttest.objects.get(id=befundId)

        if "flexion_oB_ikk" in request.POST:
            selected_befund.flexion_oB = request.POST.get("flexion_oB_ikk")
        if "flexion_kann_nicht_gehalten_werden_ikk" in request.POST:
            selected_befund.flexion_kann_nicht_gehalten_werden = request.POST.get(
                "flexion_kann_nicht_gehalten_werden_ikk"
            )
        if "extension_oB_ikk" in request.POST:
            selected_befund.extension_oB = request.POST.get("extension_oB_ikk")
        if "extension_kann_nicht_gehalten_werden_ikk" in request.POST:
            selected_befund.extension_kann_nicht_gehalten_werden = request.POST.get(
                "extension_kann_nicht_gehalten_werden_ikk"
            )

        selected_befund.save()

    if befund == "muskelfunktionspruefung":
        selected_befund = models.Muskelfunktionspruefung.objects.get(id=befundId)

        # Update Flexion fields
        if "flexion_1_mfk" in request.POST:
            selected_befund.flexion_1 = request.POST.get("flexion_1_mfk")
        if "flexion_2_mfk" in request.POST:
            selected_befund.flexion_2 = request.POST.get("flexion_2_mfk")
        if "flexion_3_mfk" in request.POST:
            selected_befund.flexion_3 = request.POST.get("flexion_3_mfk")
        if "flexion_4_mfk" in request.POST:
            selected_befund.flexion_4 = request.POST.get("flexion_4_mfk")
        if "flexion_5_mfk" in request.POST:
            selected_befund.flexion_5 = request.POST.get("flexion_5_mfk")

        # Update Extension fields
        if "extension_1_mfk" in request.POST:
            selected_befund.extension_1 = request.POST.get("extension_1_mfk")
        if "extension_2_mfk" in request.POST:
            selected_befund.extension_2 = request.POST.get("extension_2_mfk")
        if "extension_3_mfk" in request.POST:
            selected_befund.extension_3 = request.POST.get("extension_3_mfk")
        if "extension_4_mfk" in request.POST:
            selected_befund.extension_4 = request.POST.get("extension_4_mfk")
        if "extension_5_mfk" in request.POST:
            selected_befund.extension_5 = request.POST.get("extension_5_mfk")

        selected_befund.save()

    if befund == "einbeinstand_60_sekunden":
        selected_befund = models.Einbeinstand60Sekunden.objects.get(id=befundId)

        if "oB_e6k" in request.POST:
            selected_befund.oB = request.POST.get("oB_e6k")
        if "kann_nicht_gehalten_werden_e6k" in request.POST:
            selected_befund.kann_nicht_gehalten_werden = request.POST.get(
                "kann_nicht_gehalten_werden_e6k"
            )

        selected_befund.save()

    if befund == "einbeinstand_30_sekunden_geschlossene_augen":
        selected_befund = models.Einbeinstand30SekundenGeschlosseneAugen.objects.get(
            id=befundId
        )

        if "oB_e3k" in request.POST:
            selected_befund.oB = request.POST.get("oB_e3k")
        if "kann_nicht_gehalten_werden_e3k" in request.POST:
            selected_befund.kann_nicht_gehalten_werden = request.POST.get(
                "kann_nicht_gehalten_werden_e3k"
            )

        selected_befund.save()

    if befund == "alltagsfunktionen":
        selected_befund = models.Alltagsfunktionen.objects.get(id=befundId)

        if "tiefe_hocke_ob_afk" in request.POST:
            print("Angekommen")
            print(request.POST.get("tiefe_hocke_ob_afk"))
            selected_befund.tiefe_hocke_ob = request.POST.get("tiefe_hocke_ob_afk")
        if "tiefe_hocke_auffaellig_afk" in request.POST:
            selected_befund.tiefe_hocke_auffaellig = request.POST.get(
                "tiefe_hocke_auffaellig_afk"
            )
        if "tiefe_hocke_bemerkung_afk" in request.POST:
            selected_befund.tiefe_hocke_bemerkung = request.POST.get(
                "tiefe_hocke_bemerkung_afk"
            )

        if "huepfen_einem_bein_ob_afk" in request.POST:
            selected_befund.huepfen_einem_bein_ob = request.POST.get(
                "huepfen_einem_bein_ob_afk"
            )
        if "huepfen_einem_bein_auffaellig_afk" in request.POST:
            selected_befund.huepfen_einem_bein_auffaellig = request.POST.get(
                "huepfen_einem_bein_auffaellig_afk"
            )
        if "huepfen_einem_bein_bemerkung_afk" in request.POST:
            selected_befund.huepfen_einem_bein_bemerkung = request.POST.get(
                "huepfen_einem_bein_bemerkung_afk"
            )

        if "ferstand_ob_afk" in request.POST:
            selected_befund.ferstand_ob = request.POST.get("ferstand_ob_afk")
        if "ferstand_auffaellig_afk" in request.POST:
            selected_befund.ferstand_auffaellig = request.POST.get(
                "ferstand_auffaellig_afk"
            )
        if "ferstand_bemerkung_afk" in request.POST:
            selected_befund.ferstand_bemerkung = request.POST.get(
                "ferstand_bemerkung_afk"
            )

        if "fersenfall_ob_afk" in request.POST:
            selected_befund.fersenfall_ob = request.POST.get("fersenfall_ob_afk")
        if "fersenfall_auffaellig_afk" in request.POST:
            selected_befund.fersenfall_auffaellig = request.POST.get(
                "fersenfall_auffaellig_afk"
            )
        if "fersenfall_bemerkung_afk" in request.POST:
            selected_befund.fersenfall_bemerkung = request.POST.get(
                "fersenfall_bemerkung_afk"
            )

        if "einbeinstand_ob_afk" in request.POST:
            selected_befund.einbeinstand_ob = request.POST.get("einbeinstand_ob_afk")
        if "einbeinstand_auffaellig_afk" in request.POST:
            selected_befund.einbeinstand_auffaellig = request.POST.get(
                "einbeinstand_auffaellig_afk"
            )
        if "einbeinstand_bemerkung_afk" in request.POST:
            selected_befund.einbeinstand_bemerkung = request.POST.get(
                "einbeinstand_bemerkung_afk"
            )

        if "treppe_ob_afk" in request.POST:
            selected_befund.treppe_ob = request.POST.get("treppe_ob_afk")
        if "treppe_auffaellig_afk" in request.POST:
            selected_befund.treppe_auffaellig = request.POST.get(
                "treppe_auffaellig_afk"
            )
        if "tiefe_hocke_bemerkung_afk" in request.POST:
            selected_befund.treppe_bemerkung = request.POST.get("treppe_bemerkung_afk")

        selected_befund.save()

    if befund == "beinlaengenmessung":
        selected_befund = models.Beinlaengenmessung.objects.get(id=befundId)

        # Update anatomische Messung
        if "anatomische_messung_rechts_blk" in request.POST:
            selected_befund.anatomische_messung_rechts = request.POST.get(
                "anatomische_messung_rechts_blk"
            )
        if "anatomische_messung_links_blk" in request.POST:
            selected_befund.anatomische_messung_links = request.POST.get(
                "anatomische_messung_links_blk"
            )

        # Update funktionelle Messung
        if "funktionelle_messung_rechts_blk" in request.POST:
            selected_befund.funktionelle_messung_rechts = request.POST.get(
                "funktionelle_messung_rechts_blk"
            )
        if "funktionelle_messung_links_blk" in request.POST:
            selected_befund.funktionelle_messung_links = request.POST.get(
                "funktionelle_messung_links_blk"
            )

        selected_befund.save()

    if befund == "quadriceps_dehnungstest":
        selected_befund = models.QuadricepsDehnungstest.objects.get(id=befundId)

        # Update ohne Befund
        if "ohne_befund_qdk" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund_qdk")

        # Update positiv auffällig
        if "positiv_auffaellig_qdk" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get(
                "positiv_auffaellig_qdk"
            )

        # Update nicht durchführbar
        if "nicht_durchfuehrbar_qdk" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar_qdk"
            )

        # Update Bemerkung
        if "bemerkung_qdk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_qdk")

        selected_befund.save()

    if befund == "m_rectus_dehnungstest":
        selected_befund = models.MRectusDehnungstest.objects.get(id=befundId)

        # Update ohne Befund
        if "ohne_befund_mrdk" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund_mrdk")
        else:
            selected_befund.ohne_befund = False

        # Update positiv auffällig
        if "positiv_auffaellig_mrdk" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get(
                "positiv_auffaellig_mrdk"
            )

        # Update nicht durchführbar
        if "nicht_durchfuehrbar_mrdk" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar_mrdk"
            )

        # Update Bemerkung
        if "bemerkung_mrdk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_mrdk")

        selected_befund.save()

    if befund == "hamstringtest":
        selected_befund = models.Hamstringtest.objects.get(id=befundId)

        # Update ohne Befund
        if "ohne_befund_hstk" in request.POST:
            selected_befund.ohne_befund = request.POST.get("ohne_befund_hstk")

        # Update positiv auffällig
        if "positiv_auffaellig_hstk" in request.POST:
            selected_befund.positiv_auffaellig = request.POST.get(
                "positiv_auffaellig_hstk"
            )

        # Update nicht durchführbar
        if "nicht_durchfuehrbar_hstk" in request.POST:
            selected_befund.nicht_durchfuehrbar = request.POST.get(
                "nicht_durchfuehrbar_hstk"
            )

        # Update Bemerkung
        if "bemerkung_hstk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_hstk")

        selected_befund.save()

    if befund == "umfangsmessung":
        selected_befund = models.Umfangsmessung.objects.get(id=befundId)

        if "messort_10cm_oberhalb_kniegelenkspalt_rechts_ufgk" in request.POST:
            selected_befund.messort_10cm_oberhalb_kniegelenkspalt_rechts = (
                request.POST.get("messort_10cm_oberhalb_kniegelenkspalt_rechts_ufgk")
            )

        if "messort_10cm_oberhalb_kniegelenkspalt_links_ufgk" in request.POST:
            selected_befund.messort_10cm_oberhalb_kniegelenkspalt_links = (
                request.POST.get("messort_10cm_oberhalb_kniegelenkspalt_links_ufgk")
            )

        if "messort_am_kniegelenkspalt_rechts_ufgk" in request.POST:
            selected_befund.messort_am_kniegelenkspalt_rechts = request.POST.get(
                "messort_am_kniegelenkspalt_rechts_ufgk"
            )

        if "messort_am_kniegelenkspalt_links_ufgk" in request.POST:
            selected_befund.messort_am_kniegelenkspalt_links = request.POST.get(
                "messort_am_kniegelenkspalt_links_ufgk"
            )

        if "messort_10cm_unterhalb_kniegelenkspalt_rechts_ufgk" in request.POST:
            selected_befund.messort_10cm_unterhalb_kniegelenkspalt_rechts = (
                request.POST.get("messort_10cm_unterhalb_kniegelenkspalt_rechts_ufgk")
            )

        if "messort_10cm_unterhalb_kniegelenkspalt_links_ufgk" in request.POST:
            selected_befund.messort_10cm_unterhalb_kniegelenkspalt_links = (
                request.POST.get("messort_10cm_unterhalb_kniegelenkspalt_links_ufgk")
            )

        if "messort_15cm_unterhalb_kniegelenkspalt_rechts_ufgk" in request.POST:
            selected_befund.messort_15cm_unterhalb_kniegelenkspalt_rechts = (
                request.POST.get("messort_15cm_unterhalb_kniegelenkspalt_rechts_ufgk")
            )

        if "messort_15cm_unterhalb_kniegelenkspalt_links_ufgk" in request.POST:
            selected_befund.messort_15cm_unterhalb_kniegelenkspalt_links = (
                request.POST.get("messort_15cm_unterhalb_kniegelenkspalt_links_ufgk")
            )

        selected_befund.save()

    if befund == "tanzende_patella":
        selected_befund = models.TanzendePatella.objects.get(id=befundId)

        if "ohne_befund_tdpk" in request.POST:
            value = request.POST.get("ohne_befund_tdpk")
            print("Tanzende ohne_befund_tdpk:")
            print(value)
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_tdpk" in request.POST:
            value = request.POST.get("positiv_auffaellig_tdpk")
            print("Tanzende positiv_auffaellig_tdpk:")
            print(value)
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_tdpk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_tdpk")
            print("Tanzende nicht_durchfuehrbar_tdpk:")
            print(value)
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_tdpk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_tdpk")

        selected_befund.save()

    if befund == "mini_erguss_test":
        selected_befund = models.MiniErgussTest.objects.get(id=befundId)

        if "ohne_befund_metk" in request.POST:
            value = request.POST.get("ohne_befund_metk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_metk" in request.POST:
            value = request.POST.get("positiv_auffaellig_metk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_metk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_metk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_metk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_metk")

        selected_befund.save()

    if befund == "glide_test":
        selected_befund = models.GlideTest.objects.get(id=befundId)

        if "ohne_befund_gdtk" in request.POST:
            value = request.POST.get("ohne_befund_gdtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_gdtk" in request.POST:
            value = request.POST.get("positiv_auffaellig_gdtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_gdtk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_gdtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_gdtk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_gdtk")

        selected_befund.save()

    if befund == "tilt_test":
        selected_befund = models.TiltTest.objects.get(id=befundId)

        if "ohne_befund_tttk" in request.POST:
            value = request.POST.get("ohne_befund_tttk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_tttk" in request.POST:
            value = request.POST.get("positiv_auffaellig_tttk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_tttk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_tttk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_tttk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_tttk")

        selected_befund.save()

    if befund == "aprehension_test":
        selected_befund = models.AprehensionTest.objects.get(id=befundId)

        if "ohne_befund_ahtk" in request.POST:
            value = request.POST.get("ohne_befund_ahtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_ahtk" in request.POST:
            value = request.POST.get("positiv_auffaellig_ahtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_ahtk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_ahtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_ahtk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_ahtk")

        selected_befund.save()

    if befund == "zohlen_zeichen":
        selected_befund = models.ZohlenZeichen.objects.get(id=befundId)

        if "ohne_befund_zlzk" in request.POST:
            value = request.POST.get("ohne_befund_zlzk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_zlzk" in request.POST:
            value = request.POST.get("positiv_auffaellig_zlzk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_zlzk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_zlzk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_zlzk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_zlzk")

        selected_befund.save()

    if befund == "facettendruckschmerztest":
        selected_befund = models.Facettendruckschmerztest.objects.get(id=befundId)

        if "ohne_befund_fdstk" in request.POST:
            value = request.POST.get("ohne_befund_fdstk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_fdstk" in request.POST:
            value = request.POST.get("positiv_auffaellig_fdstk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_fdstk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_fdstk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_fdstk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_fdstk")

        selected_befund.save()

    if befund == "valgus_test":
        selected_befund = models.ValgusTest.objects.get(id=befundId)

        if "ohne_befund_vgtk" in request.POST:
            value = request.POST.get("ohne_befund_vgtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_vgtk" in request.POST:
            value = request.POST.get("positiv_auffaellig_vgtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_vgtk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_vgtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_vgtk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_vgtk")

        selected_befund.save()

    if befund == "varus_test":
        selected_befund = models.VarusTest.objects.get(id=befundId)

        if "ohne_befund_vrtk" in request.POST:
            value = request.POST.get("ohne_befund_vrtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_vrtk" in request.POST:
            value = request.POST.get("positiv_auffaellig_vrtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_vrtk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_vrtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_vrtk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_vrtk")

        selected_befund.save()

    if befund == "lachmann_test":
        selected_befund = models.LachmannTest.objects.get(id=befundId)

        if "ohne_befund_lmtk" in request.POST:
            value = request.POST.get("ohne_befund_lmtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_lmtk" in request.POST:
            value = request.POST.get("positiv_auffaellig_lmtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_lmtk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_lmtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_lmtk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_lmtk")

        selected_befund.save()

    if befund == "vordere_schublade":
        selected_befund = models.VordereSchublade.objects.get(id=befundId)

        if "ohne_befund_vdsk" in request.POST:
            value = request.POST.get("ohne_befund_vdsk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_vdsk" in request.POST:
            value = request.POST.get("positiv_auffaellig_vdsk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_vdsk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_vdsk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_vdsk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_vdsk")

        selected_befund.save()

    if befund == "pivot_shift_test":
        selected_befund = models.PivotShiftTest.objects.get(id=befundId)

        if "ohne_befund_pstk" in request.POST:
            value = request.POST.get("ohne_befund_pstk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_pstk" in request.POST:
            value = request.POST.get("positiv_auffaellig_pstk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_pstk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_pstk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_pstk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_pstk")

        selected_befund.save()

    if befund == "hintere_schublade":
        selected_befund = models.HintereSchublade.objects.get(id=befundId)

        if "ohne_befund_htsk" in request.POST:
            value = request.POST.get("ohne_befund_htsk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_htsk" in request.POST:
            value = request.POST.get("positiv_auffaellig_htsk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_htsk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_htsk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_htsk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_htsk")

        selected_befund.save()

    if befund == "gravitiy_sign":
        selected_befund = models.GravitiySign.objects.get(id=befundId)

        if "ohne_befund_gvsk" in request.POST:
            value = request.POST.get("ohne_befund_gvsk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_gvsk" in request.POST:
            value = request.POST.get("positiv_auffaellig_gvsk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_gvsk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_gvsk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_gvsk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_gvsk")

        selected_befund.save()

    if befund == "loomers_test":
        selected_befund = models.LoomersTest.objects.get(id=befundId)

        if "ohne_befund_lmtk" in request.POST:
            value = request.POST.get("ohne_befund_lmtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_lmtk" in request.POST:
            value = request.POST.get("positiv_auffaellig_lmtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_lmtk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_lmtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_lmtk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_lmtk")

        selected_befund.save()

    if befund == "steinmann1":
        selected_befund = models.Steinmann1.objects.get(id=befundId)

        if "ohne_befund_st1k" in request.POST:
            value = request.POST.get("ohne_befund_st1k")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_st1k" in request.POST:
            value = request.POST.get("positiv_auffaellig_st1k")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_st1k" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_st1k")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_st1k" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_st1k")

        selected_befund.save()

    if befund == "steinmann3":
        selected_befund = models.Steinmann3.objects.get(id=befundId)

        if "ohne_befund_st3k" in request.POST:
            value = request.POST.get("ohne_befund_st3k")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_st3k" in request.POST:
            value = request.POST.get("positiv_auffaellig_st3k")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_st3k" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_st3k")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_st3k" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_st3k")

        selected_befund.save()

    if befund == "theslay_test":
        selected_befund = models.TheslayTest.objects.get(id=befundId)

        if "ohne_befund_thtk" in request.POST:
            value = request.POST.get("ohne_befund_thtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_thtk" in request.POST:
            value = request.POST.get("positiv_auffaellig_thtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_thtk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_thtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_thtk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_thtk")

        selected_befund.save()

    if befund == "mac_murray_test":
        selected_befund = models.MacMurrayTest.objects.get(id=befundId)

        if "ohne_befund_mmtk" in request.POST:
            value = request.POST.get("ohne_befund_mmtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_mmtk" in request.POST:
            value = request.POST.get("positiv_auffaellig_mmtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_mmtk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_mmtk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_mmtk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_mmtk")

        selected_befund.save()

    if befund == "payr_zeichen":
        selected_befund = models.PayrZeichen.objects.get(id=befundId)

        if "ohne_befund_pyzk" in request.POST:
            value = request.POST.get("ohne_befund_pyzk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_pyzk" in request.POST:
            value = request.POST.get("positiv_auffaellig_pyzk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_pyzk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_pyzk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_pyzk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_pyzk")

        selected_befund.save()

    if befund == "apley_zeichen":
        selected_befund = models.ApleyZeichen.objects.get(id=befundId)

        if "ohne_befund_ayzk" in request.POST:
            value = request.POST.get("ohne_befund_ayzk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_ayzk" in request.POST:
            value = request.POST.get("positiv_auffaellig_ayzk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_ayzk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_ayzk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_ayzk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_ayzk")

        selected_befund.save()

    if befund == "medio_patellarer_plica_test":
        selected_befund = models.MedioPatellarerPlicaTest.objects.get(id=befundId)

        if "ohne_befund_mpptk" in request.POST:
            value = request.POST.get("ohne_befund_mpptk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_mpptk" in request.POST:
            value = request.POST.get("positiv_auffaellig_mpptk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_mpptk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_mpptk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_mpptk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_mpptk")

        selected_befund.save()

    if befund == "hughston_plica_test":
        selected_befund = models.HughstonPlicaTest.objects.get(id=befundId)

        if "ohne_befund_hgptk" in request.POST:
            value = request.POST.get("ohne_befund_hgptk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.ohne_befund = value == "True" or value == "1"

        if "positiv_auffaellig_hgptk" in request.POST:
            value = request.POST.get("positiv_auffaellig_hgptk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.positiv_auffaellig = value == "True" or value == "1"

        if "nicht_durchfuehrbar_hgptk" in request.POST:
            value = request.POST.get("nicht_durchfuehrbar_hgptk")
            if value in ["True", "False", "1", "0"]:
                selected_befund.nicht_durchfuehrbar = value == "True" or value == "1"

        if "bemerkung_hgptk" in request.POST:
            selected_befund.bemerkung = request.POST.get("bemerkung_hgptk")

        selected_befund.save()

    if befund == "red_flag_screening_schulter":
        selected_befund = models.RedFlagScreeningSchulter.objects.get(
            id=befundId
        )
        model_fields = models.RedFlagScreeningSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "aktive_beweglichkeit_schulter":
        selected_befund = models.AktiveBeweglichkeitSchulter.objects.get(id=befundId)

        fields = [
            "links_abs",
            "rechts_abs",
            "flexion_ob_abs",
            "extension_ob_abs",
            "abduktion_ob_abs",
            "adduktion_ob_abs",
            "innenrotation_ob_abs",
            "außenrotation_ob_abs",
            "flexion_leicht_begrenzt_abs",
            "extension_leicht_begrenzt_abs",
            "abduktion_leicht_begrenzt_abs",
            "adduktion_leicht_begrenzt_abs",
            "innenrotation_leicht_begrenzt_abs",
            "außenrotation_leicht_begrenzt_abs",
            "flexion_moderat_begrenzt_abs",
            "extension_moderat_begrenzt_abs",
            "abduktion_moderat_begrenzt_abs",
            "adduktion_moderat_begrenzt_abs",
            "innenrotation_moderat_begrenzt_abs",
            "außenrotation_moderat_begrenzt_abs",
            "flexion_stark_begrenzt_abs",
            "extension_stark_begrenzt_abs",
            "abduktion_stark_begrenzt_abs",
            "adduktion_stark_begrenzt_abs",
            "innenrotation_stark_begrenzt_abs",
            "außenrotation_stark_begrenzt_abs",
            "flexion_schmerzhaft_abs",
            "extension_schmerzhaft_abs",
            "abduktion_schmerzhaft_abs",
            "adduktion_schmerzhaft_abs",
            "innenrotation_schmerzhaft_abs",
            "außenrotation_schmerzhaft_abs",
            "flexion_unkoordiniert_gehemmt_abs",
            "extension_unkoordiniert_gehemmt_abs",
            "abduktion_unkoordiniert_gehemmt_abs",
            "adduktion_unkoordiniert_gehemmt_abs",
            "innenrotation_unkoordiniert_gehemmt_abs",
            "außenrotation_unkoordiniert_gehemmt_abs",
        ]

        for field in fields:
            if field in request.POST:
                value = request.POST.get(field)
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")

        if "bemerkung_abs" in request.POST:
            selected_befund.bemerkung_abs = request.POST.get("bemerkung_abs")

        return HttpResponse("Updated Succesfully")

    if befund == "passive_beweglichkeit_schulter":
        selected_befund = models.PassiveBeweglichkeitSchulter.objects.get(id=befundId)

        fields = [
            "links_pbs",
            "rechts_pbs",
            "flexion_ob_pbs",
            "extension_ob_pbs",
            "abduktion_ob_pbs",
            "adduktion_ob_pbs",
            "innenrotation_ob_pbs",
            "außenrotation_ob_pbs",
            "flexion_leicht_begrenzt_pbs",
            "extension_leicht_begrenzt_pbs",
            "abduktion_leicht_begrenzt_pbs",
            "adduktion_leicht_begrenzt_pbs",
            "innenrotation_leicht_begrenzt_pbs",
            "außenrotation_leicht_begrenzt_pbs",
            "flexion_moderat_begrenzt_pbs",
            "extension_moderat_begrenzt_pbs",
            "abduktion_moderat_begrenzt_pbs",
            "adduktion_moderat_begrenzt_pbs",
            "innenrotation_moderat_begrenzt_pbs",
            "außenrotation_moderat_begrenzt_pbs",
            "flexion_stark_begrenzt_pbs",
            "extension_stark_begrenzt_pbs",
            "abduktion_stark_begrenzt_pbs",
            "adduktion_stark_begrenzt_pbs",
            "innenrotation_stark_begrenzt_pbs",
            "außenrotation_stark_begrenzt_pbs",
            "flexion_schmerzhaft_pbs",
            "extension_schmerzhaft_pbs",
            "abduktion_schmerzhaft_pbs",
            "adduktion_schmerzhaft_pbs",
            "innenrotation_schmerzhaft_pbs",
            "außenrotation_schmerzhaft_pbs",
            "flexion_unkoordiniert_gehemmt_pbs",
            "extension_unkoordiniert_gehemmt_pbs",
            "abduktion_unkoordiniert_gehemmt_pbs",
            "adduktion_unkoordiniert_gehemmt_pbs",
            "innenrotation_unkoordiniert_gehemmt_pbs",
            "außenrotation_unkoordiniert_gehemmt_pbs",
        ]

        for field in fields:
            if field in request.POST:
                value = request.POST.get(field)
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")

        if "bemerkung_pbs" in request.POST:
            selected_befund.bemerkung_pbs = request.POST.get("bemerkung_pbs")

        return HttpResponse("Updated Succesfully")

    if befund == "beweglichkeitsmessung_schulter":
        selected_befund = models.BeweglichkeitsmessungSchulter.objects.get(id=befundId)

        boolean_fields = ["links_bms", "rechts_bms"]
        char_fields = [
            "flexion_extension_bms",
            "abduktion_adduktion_bms",
            "transversale_flexion_extension_bms",
            "innen_außenrotation_nullstellung_bms",
            "innen_außenrotation_90_grad_bms",
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")

        for field in char_fields:
            if field in request.POST:
                selected_befund_value = request.POST.get(field)
                if selected_befund_value:
                    setattr(selected_befund, field, selected_befund_value)

        selected_befund.save()
        return HttpResponse("Updated Succesfully")

    if befund == "c_sar":
        selected_befund = models.CopenhagenShoulderAbductionRating.objects.get(
            id=befundId
        )
        model_fields = models.CopenhagenShoulderAbductionRating._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "posteriore_schultersteifheit":
        selected_befund = models.PosterioreSchultersteifheit.objects.get(id=befundId)
        model_fields = models.PosterioreSchultersteifheit._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "isometrischer_krafttest_schulter":
        selected_befund = models.IsometrischerKrafttestSchulter.objects.get(id=befundId)
        model_fields = models.IsometrischerKrafttestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "muskelfunktionspruefung_schulter":
        selected_befund = models.MuskelfunktionspruefungSchulter.objects.get(
            id=befundId
        )
        model_fields = models.MuskelfunktionspruefungSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "feds_kalassifikation":
        selected_befund = models.FEDSKalassifikationSchulter.objects.get(id=befundId)
        model_fields = models.FEDSKalassifikationSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "anterior_aprehension_test":
        selected_befund = models.AnteriorAprehensionTestSchulter.objects.get(
            id=befundId
        )
        model_fields = models.AnteriorAprehensionTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "relocation_test_nach_jobe":
        selected_befund = models.RelocationTestnachJobeSchulter.objects.get(id=befundId)
        model_fields = models.RelocationTestnachJobeSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "surprise_release_test":
        selected_befund = models.SurpriseReleaseTestSchulter.objects.get(id=befundId)
        model_fields = models.SurpriseReleaseTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "anterior_drawer_test":
        selected_befund = models.AnteriorDrawerTestSchulter.objects.get(id=befundId)
        model_fields = models.AnteriorDrawerTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "sulcustest":
        selected_befund = models.SulcusTestSchulter.objects.get(id=befundId)
        model_fields = models.SulcusTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "posterior_aprehension_test":
        selected_befund = models.PosteriorAprehensionTestSchulter.objects.get(
            id=befundId
        )
        model_fields = models.PosteriorAprehensionTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "jerk_test":
        selected_befund = models.JerkTestSchulter.objects.get(id=befundId)
        model_fields = models.JerkTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "kim_test":
        selected_befund = models.KimTestSchulter.objects.get(id=befundId)
        model_fields = models.KimTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "posterior_drawer_test":
        selected_befund = models.PosteriorDrawerTestSchulter.objects.get(id=befundId)
        model_fields = models.PosteriorDrawerTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "load_and_shift_test":
        selected_befund = models.LoadAndShiftTestSchulter.objects.get(id=befundId)
        model_fields = models.LoadAndShiftTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "sulcus_zeichen":
        selected_befund = models.SulcusZeichenSchulter.objects.get(id=befundId)
        model_fields = models.SulcusZeichenSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "coudance_walch_test":
        selected_befund = models.CoudanceWalchTestSchulter.objects.get(id=befundId)
        model_fields = models.CoudanceWalchTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "gargey_test":
        selected_befund = models.GargeyTestSchulter.objects.get(id=befundId)
        model_fields = models.GargeyTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "nervenmobilitaetstestungen_bpnt":
        selected_befund = models.NervenmobilitaetstestungenSchulter.objects.get(
            id=befundId
        )
        model_fields = models.NervenmobilitaetstestungenSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "schnell_anamnese_frozen_shoulder":
        selected_befund = models.SchnellAnamneseFrozenShoulder.objects.get(id=befundId)
        model_fields = models.SchnellAnamneseFrozenShoulder._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "adsons_test":
        selected_befund = models.AdsonsTestSchulter.objects.get(id=befundId)
        model_fields = models.AdsonsTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "wrights_test":
        selected_befund = models.WrightsTestHyperabduktionSchulter.objects.get(
            id=befundId
        )
        model_fields = models.WrightsTestHyperabduktionSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "edens_test":
        selected_befund = models.EdensTestCostoclavikulaererDruckSchulter.objects.get(
            id=befundId
        )
        model_fields = (
            models.EdensTestCostoclavikulaererDruckSchulter._meta.get_fields()
        )
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "east_test":
        selected_befund = models.ElevatedArmStressTestEASTSchulter.objects.get(
            id=befundId
        )
        model_fields = models.ElevatedArmStressTestEASTSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "cyrax_release_test":
        selected_befund = models.CyraxReleaseTestSchulter.objects.get(id=befundId)
        model_fields = models.CyraxReleaseTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "morley_compression_test":
        selected_befund = models.MorleyCmpressionTestSchulter.objects.get(id=befundId)
        model_fields = models.MorleyCmpressionTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "irritierbarkeit_schulter_star":
        selected_befund = (
            models.IrritierbarkeitderSchulterAnlehnungSTASchulterDiagnose.objects.get(
                id=befundId
            )
        )
        model_fields = (
            models.IrritierbarkeitderSchulterAnlehnungSTASchulterDiagnose._meta.get_fields()
        )
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "alltagsfunktionen_schulter":
        selected_befund = models.AlltagsfunktionenSchulter.objects.get(id=befundId)
        model_fields = models.AlltagsfunktionenSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "umfangsmessung_arm":
        selected_befund = models.UmfangsmessungArm.objects.get(id=befundId)
        model_fields = models.UmfangsmessungArm._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "scapula_assistenstest_sat":
        selected_befund = models.ScapulaAssistenstesSATSchulter.objects.get(id=befundId)
        model_fields = models.ScapulaAssistenstesSATSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "lateral_scapula_slide_test":
        selected_befund = models.LateralerScapulaSlideTestSchulter.objects.get(
            id=befundId
        )
        model_fields = models.LateralerScapulaSlideTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "scapula_retraction_test_srt":
        selected_befund = models.ScapulaRetractionTestSRTSchulter.objects.get(
            id=befundId
        )
        model_fields = models.ScapulaRetractionTestSRTSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "lateraler_scapula_slide_test":
        selected_befund = models.LateralerScapulaSlideTestSchulter.objects.get(
            id=befundId
        )
        model_fields = models.LateralerScapulaSlideTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "jobe_test":
        selected_befund = models.JobeTestSchulter.objects.get(id=befundId)
        model_fields = models.JobeTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "null_grad_adduktionstest":
        selected_befund = models.NullGradAdduktionstestSchulter.objects.get(id=befundId)
        model_fields = models.NullGradAdduktionstestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "drop_arm_zeichen":
        selected_befund = models.DropArmZeichenSchulter.objects.get(id=befundId)
        model_fields = models.DropArmZeichenSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "lift_off_test":
        selected_befund = models.LiftOffTestSchulter.objects.get(id=befundId)
        model_fields = models.LiftOffTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "belly_press_belly_off_zeichen":
        selected_befund = models.BellyPressBellyOffZeichenSchulter.objects.get(
            id=befundId
        )
        model_fields = models.BellyPressBellyOffZeichenSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "bear_hug_test":
        selected_befund = models.BearHugTestSchulter.objects.get(id=befundId)
        model_fields = models.BearHugTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "null_grad_aussenrotationstest":
        selected_befund = models.NullGradAußenrotationstestSchulter.objects.get(
            id=befundId
        )
        model_fields = models.NullGradAußenrotationstestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "painful_arc":
        selected_befund = models.PainfulArcSchulter.objects.get(id=befundId)
        model_fields = models.PainfulArcSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "hawkins_kennedy_test":
        selected_befund = models.HawkinsKennedyTestSchulter.objects.get(id=befundId)
        model_fields = models.HawkinsKennedyTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "neer_test":
        selected_befund = models.NeerTestSchulter.objects.get(id=befundId)
        model_fields = models.NeerTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "unspezifischer_bicepssehenen_test":
        selected_befund = models.UnspezifischerBicepssehenenTestSchulter.objects.get(
            id=befundId
        )
        model_fields = models.UnspezifischerBicepssehenenTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "yergason":
        selected_befund = models.YergasonSchulter.objects.get(id=befundId)
        model_fields = models.YergasonSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "speedys_test":
        selected_befund = models.SpeedysTestSchulter.objects.get(id=befundId)
        model_fields = models.SpeedysTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "o_briens_test":
        selected_befund = models.OBriensTestSchulter.objects.get(id=befundId)
        model_fields = models.OBriensTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "biceps_load_test":
        selected_befund = models.BicepsLoadTestSchulter.objects.get(id=befundId)
        model_fields = models.BicepsLoadTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "supine_flexion_resitance_test":
        selected_befund = models.SupineFlexionResitanceTestSchulter.objects.get(
            id=befundId
        )
        model_fields = models.SupineFlexionResitanceTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    if befund == "crank_test":
        selected_befund = models.CrankTestSchulter.objects.get(id=befundId)
        model_fields = models.CrankTestSchulter._meta.get_fields()
        field_names = [
            field.name for field in model_fields if field.name not in excluded_fields
        ]
        boolean_fields = [
            field.name
            for field in model_fields
            if isinstance(field, modelsdb.BooleanField)
        ]

        for field in boolean_fields:
            if field in request.POST:
                value = request.POST.get(field)
                print(f"{field}: {value}")  # Debugging output
                if value in ["True", "False", "1", "0"]:
                    setattr(selected_befund, field, value == "True" or value == "1")
                    print(
                        f"Set {field} to {getattr(selected_befund, field)}"
                    )  # Debugging output

        for field_name in field_names:
            if field_name not in boolean_fields and field_name in request.POST:
                value = request.POST.get(field_name)
                field_object = next(
                    (f for f in model_fields if f.name == field_name), None
                )

                if isinstance(field_object, modelsdb.CharField):
                    setattr(selected_befund, field_name, value)
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.IntegerField):
                    setattr(selected_befund, field_name, int(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                elif isinstance(field_object, modelsdb.FloatField):
                    setattr(selected_befund, field_name, float(value))
                    print(
                        f"Set {field_name} to {getattr(selected_befund, field_name)}"
                    )  # Debugging output
                # Hier kannst du weitere Feldtypen prüfen und entsprechend behandeln

        selected_befund.save()

    return HttpResponse("Updated Successfully")


@login_required(login_url="login")
def new_personal_befund(request, id=None):
    if id == None:
        return HttpResponse("Not valid")
    befund = request.POST.get("befund")

    if befund == "fragenevaluation_icf":
        models.FragenevaluationNachICFKategorien.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "fragenevaluation_bio_psycho_sozial_krankheitsmodell":
        models.FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "w_fragen":
        models.FragenevaluationenNachDen7WFragen.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "standart_befund":
        models.StandartBefund.objects.create(created_for=id, created_by=request.user)
    if befund == "stand_reha_phase":
        models.StandDerReHaPhase.objects.create(created_for=id, created_by=request.user)
    if befund == "nebenerkrankungen_medikamente":
        models.NebenerkrankungenMedikamente.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "historia_morbis":
        models.HistoriaMorbis.objects.create(created_for=id, created_by=request.user)
    if befund == "nrs_numeric_rating_scale":
        models.NrsNumericRatingScale.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "aktive_beweglichkeit":
        models.AktiveBeweglichkeit.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "passive_beweglichkeit":
        models.PassiveBeweglichkeit.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "beweglichkeitsmessung":
        models.BeweglichkeitsmessungKnie.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "isometrischer_krafttest":
        models.IsometrischerKrafttest.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "muskelfunktionspruefung":
        models.Muskelfunktionspruefung.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "einbeinstand_60_sekunden":
        models.Einbeinstand60Sekunden.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "einbeinstand_30_sekunden_geschlossene_augen":
        models.Einbeinstand30SekundenGeschlosseneAugen.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "alltagsfunktionen":
        models.Alltagsfunktionen.objects.create(created_by=request.user, created_for=id)
    if befund == "beinlaengenmessung":
        models.Beinlaengenmessung.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "quadriceps_dehnungstest":
        models.QuadricepsDehnungstest.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "m_rectus_dehnungstest":
        models.MRectusDehnungstest.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "hamstringtest":
        models.Hamstringtest.objects.create(created_by=request.user, created_for=id)
    if befund == "umfangsmessung":
        models.Umfangsmessung.objects.create(created_by=request.user, created_for=id)
    if befund == "tanzende_patella":
        models.TanzendePatella.objects.create(created_by=request.user, created_for=id)
    if befund == "mini_erguss_test":
        models.MiniErgussTest.objects.create(created_by=request.user, created_for=id)
    if befund == "glide_test":
        models.GlideTest.objects.create(created_by=request.user, created_for=id)
    if befund == "tilt_test":
        models.TiltTest.objects.create(created_by=request.user, created_for=id)
    if befund == "aprehension_test":
        models.AprehensionTest.objects.create(created_by=request.user, created_for=id)
    if befund == "zohlen_zeichen":
        models.ZohlenZeichen.objects.create(created_by=request.user, created_for=id)
    if befund == "facettendruckschmerztest":
        models.Facettendruckschmerztest.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "valgus_test":
        models.ValgusTest.objects.create(created_by=request.user, created_for=id)
    if befund == "varus_test":
        models.VarusTest.objects.create(created_by=request.user, created_for=id)
    if befund == "lachmann_test":
        models.LachmannTest.objects.create(created_by=request.user, created_for=id)
    if befund == "vordere_schublade":
        models.VordereSchublade.objects.create(created_by=request.user, created_for=id)
    if befund == "pivot_shift_test":
        models.PivotShiftTest.objects.create(created_by=request.user, created_for=id)
    if befund == "hintere_schublade":
        models.HintereSchublade.objects.create(created_by=request.user, created_for=id)
    if befund == "gravitiy_sign":
        models.GravitiySign.objects.create(created_by=request.user, created_for=id)
    if befund == "loomers_test":
        models.LoomersTest.objects.create(created_by=request.user, created_for=id)
    if befund == "steinmann1":
        models.Steinmann1.objects.create(created_by=request.user, created_for=id)
    if befund == "steinmann3":
        models.Steinmann3.objects.create(created_by=request.user, created_for=id)
    if befund == "theslay_test":
        models.TheslayTest.objects.create(created_by=request.user, created_for=id)
    if befund == "mac_murray_test":
        models.MacMurrayTest.objects.create(created_by=request.user, created_for=id)
    if befund == "payr_zeichen":
        models.PayrZeichen.objects.create(created_by=request.user, created_for=id)
    if befund == "apley_zeichen":
        models.ApleyZeichen.objects.create(created_by=request.user, created_for=id)
    if befund == "medio_patellarer_plica_test":
        models.MedioPatellarerPlicaTest.objects.create(
            created_by=request.user, created_for=id
        )
    if befund == "hughston_plica_test":
        models.HughstonPlicaTest.objects.create(created_by=request.user, created_for=id)

    if befund == "red_flag_screening_schulter":

        models.RedFlagScreeningSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "aktive_beweglichkeit_schulter":

        models.AktiveBeweglichkeitSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "passive_beweglichkeit_schulter":

        models.PassiveBeweglichkeitSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "beweglichkeitsmessung_schulter":

        models.BeweglichkeitsmessungSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "c_sar":

        models.CopenhagenShoulderAbductionRating.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "posteriore_schultersteifheit":

        models.PosterioreSchultersteifheit.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "isometrischer_krafttest_schulter":

        models.IsometrischerKrafttestSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "muskelfunktionspruefung_schulter":

        models.MuskelfunktionspruefungSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "feds_kalassifikation":

        models.FEDSKalassifikationSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "anterior_aprehension_test":

        models.AnteriorAprehensionTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "relocation_test_nach_jobe":

        models.RelocationTestnachJobeSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "surprise_release_test":

        models.SurpriseReleaseTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "anterior_drawer_test":

        models.AnteriorDrawerTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "sulcustest":

        models.SulcusTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "posterior_aprehension_test":

        models.PosteriorAprehensionTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "kim_test":

        models.KimTestSchulter.objects.create(created_for=id, created_by=request.user)

    if befund == "jerk_test":

        models.JerkTestSchulter.objects.create(created_for=id, created_by=request.user)

    if befund == "load_and_shift_test":

        models.LoadAndShiftTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "sulcus_zeichen":

        models.SulcusZeichenSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "schnell_anamnese_frozen_shoulder":

        models.SchnellAnamneseFrozenShoulder.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "adsons_test":

        models.AdsonsTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "coudance_walch_test":

        models.CoudanceWalchTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "gargey_test":

        models.GargeyTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "nervenmobilitaetstestungen_bpnt":

        models.NervenmobilitaetstestungenSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "wrights_test":

        models.WrightsTestHyperabduktionSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "edens_test":

        models.EdensTestCostoclavikulaererDruckSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "east_test":

        models.ElevatedArmStressTestEASTSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "cyrax_release_test":

        models.CyraxReleaseTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "morley_compression_test":

        models.MorleyCmpressionTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "irritierbarkeit_schulter_star":

        models.IrritierbarkeitderSchulterAnlehnungSTASchulterDiagnose.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "alltagsfunktionen_schulter":

        models.AlltagsfunktionenSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "umfangsmessung_arm":

        models.UmfangsmessungArm.objects.create(created_for=id, created_by=request.user)

    if befund == "scapula_assistenstest_sat":

        models.ScapulaAssistenstesSATSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "lateral_scapula_slide_test":

        models.LateralerScapulaSlideTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "scapula_retraction_test_srt":

        models.ScapulaRetractionTestSRTSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "lateraler_scapula_slide_test":

        models.LateralerScapulaSlideTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "jobe_test":

        models.JobeTestSchulter.objects.create(created_for=id, created_by=request.user)
    if befund == "null_grad_adduktionstest":

        models.NullGradAdduktionstestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "drop_arm_zeichen":

        models.DropArmZeichenSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "lift_off_test":

        models.LiftOffTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "belly_press_belly_off_zeichen":

        models.BellyPressBellyOffZeichenSchulter.objects.create(
            created_for=id, created_by=request.user
        )

    if befund == "bear_hug_test":

        models.BearHugTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "null_grad_aussenrotationstest":
        models.NullGradAußenrotationstestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "painful_arc":

        models.PainfulArcSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "hawkins_kennedy_test":

        models.HawkinsKennedyTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "neer_test":

        models.NeerTestSchulter.objects.create(created_for=id, created_by=request.user)
    if befund == "unspezifischer_bicepssehenen_test":

        models.UnspezifischerBicepssehenenTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "yergason":

        models.YergasonSchulter.objects.create(created_for=id, created_by=request.user)
    if befund == "speedys_test":

        models.SpeedysTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "o_briens_test":

        models.OBriensTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "biceps_load_test":

        models.BicepsLoadTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    if befund == "supine_flexion_resitance_test":

        models.SupineFlexionResitanceTestSchulter.objects.create(
            created_for=id, created_by=request.user
        )
    befund = request.POST.get("befund")

    if befund == "crank_test":

        models.CrankTestSchulter.objects.create(created_for=id, created_by=request.user)
    return HttpResponse("Updated Succesfully")


@login_required(login_url="login")
def delete_personal_befund(request, id=None, befundId=None):
    if id == None:
        return HttpResponse("Not valid")
    befund = request.POST.get("befund")
    if befund == "fragenevaluation_icf":
        selected_befund = models.FragenevaluationNachICFKategorien.objects.get(
            id=befundId
        )
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "fragenevaluation_bio_psycho_sozial_krankheitsmodell":
        selected_befund = models.FragenevaluationenNachDemBioPsychoSozialenKrankheitsmodell.objects.get(
            id=befundId
        )
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "w_fragen":
        selected_befund = models.FragenevaluationenNachDen7WFragen.objects.get(
            id=befundId
        )
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "standart_befund":
        selected_befund = models.StandartBefund.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "stand_reha_phase":
        selected_befund = models.StandDerReHaPhase.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "nebenerkrankungen_medikamente":
        selected_befund = models.NebenerkrankungenMedikamente.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()
    if befund == "historia_morbis":
        selected_befund = models.HistoriaMorbis.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "nrs_numeric_rating_scale":
        selected_befund = models.NrsNumericRatingScale.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "aktive_beweglichkeit":
        selected_befund = models.AktiveBeweglichkeit.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "passive_beweglichkeit":
        selected_befund = models.PassiveBeweglichkeit.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "beweglichkeitsmessung":
        selected_befund = models.BeweglichkeitsmessungKnie.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "isometrischer_krafttest":
        selected_befund = models.IsometrischerKrafttest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "muskelfunktionspruefung":
        selected_befund = models.Muskelfunktionspruefung.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "einbeinstand_60_sekunden":
        selected_befund = models.Einbeinstand60Sekunden.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "einbeinstand_30_sekunden_geschlossene_augen":
        selected_befund = models.Einbeinstand30SekundenGeschlosseneAugen.objects.get(
            id=befundId
        )
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "alltagsfunktionen":
        selected_befund = models.Alltagsfunktionen.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "beinlaengenmessung":
        selected_befund = models.Beinlaengenmessung.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "quadriceps_dehnungstest":
        selected_befund = models.QuadricepsDehnungstest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "m_rectus_dehnungstest":
        selected_befund = models.MRectusDehnungstest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "hamstringtest":
        selected_befund = models.Hamstringtest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "umfangsmessung":
        selected_befund = models.Umfangsmessung.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "tanzende_patella":
        selected_befund = models.TanzendePatella.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "mini_erguss_test":
        selected_befund = models.MiniErgussTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "glide_test":
        selected_befund = models.GlideTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "tilt_test":
        selected_befund = models.TiltTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "aprehension_test":
        selected_befund = models.AprehensionTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "zohlen_zeichen":
        selected_befund = models.ZohlenZeichen.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "facettendruckschmerztest":
        selected_befund = models.Facettendruckschmerztest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "valgus_test":
        selected_befund = models.ValgusTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "varus_test":
        selected_befund = models.VarusTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "lachmann_test":
        selected_befund = models.LachmannTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "vordere_schublade":
        selected_befund = models.VordereSchublade.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "pivot_shift_test":
        selected_befund = models.PivotShiftTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "hintere_schublade":
        selected_befund = models.HintereSchublade.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "gravitiy_sign":
        selected_befund = models.GravitiySign.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "loomers_test":
        selected_befund = models.LoomersTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "steinmann1":
        selected_befund = models.Steinmann1.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "steinmann3":
        selected_befund = models.Steinmann3.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "theslay_test":
        selected_befund = models.TheslayTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "mac_murray_test":
        selected_befund = models.MacMurrayTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "payr_zeichen":
        selected_befund = models.PayrZeichen.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "apley_zeichen":
        selected_befund = models.ApleyZeichen.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "medio_patellarer_plica_test":
        selected_befund = models.MedioPatellarerPlicaTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "hughston_plica_test":
        selected_befund = models.HughstonPlicaTest.objects.get(id=befundId)
        if request.user == selected_befund.created_by:
            selected_befund.delete()

    if befund == "red_flag_screening_schulter":

        selected_befund = models.RedFlagScreeningSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "aktive_beweglichkeit_schulter":

        selected_befund = models.AktiveBeweglichkeitSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "passive_beweglichkeit_schulter":

        selected_befund = models.PassiveBeweglichkeitSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "beweglichkeitsmessung_schulter":

        selected_befund = models.BeweglichkeitsmessungSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "c_sar":

        selected_befund = models.CopenhagenShoulderAbductionRating.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "posteriore_schultersteifheit":

        selected_befund = models.PosterioreSchultersteifheit.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "isometrischer_krafttest_schulter":

        selected_befund = models.IsometrischerKrafttestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "muskelfunktionspruefung_schulter":

        selected_befund = models.MuskelfunktionspruefungSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "feds_kalassifikation":

        selected_befund = models.FEDSKalassifikationSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "anterior_aprehension_test":

        selected_befund = models.AnteriorAprehensionTestSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "relocation_test_nach_jobe":

        selected_befund = models.RelocationTestnachJobeSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "surprise_release_test":

        selected_befund = models.SurpriseReleaseTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "anterior_drawer_test":

        selected_befund = models.AnteriorDrawerTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "sulcustest":

        selected_befund = models.SulcusTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "posterior_aprehension_test":

        selected_befund = models.PosteriorAprehensionTestSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "jerk_test":

        selected_befund = models.JerkTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "kim_test":

        selected_befund = models.KimTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "load_and_shift_test":

        selected_befund = models.LoadAndShiftTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "sulcus_zeichen":

        selected_befund = models.SulcusZeichenSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "coudance_walch_test":

        selected_befund = models.CoudanceWalchTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "gargey_test":

        selected_befund = models.GargeyTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "nervenmobilitaetstestungen_bpnt":

        selected_befund = models.NervenmobilitaetstestungenSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "schnell_anamnese_frozen_shoulder":

        selected_befund = models.SchnellAnamneseFrozenShoulder.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "adsons_test":

        selected_befund = models.AdsonsTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "wrights_test":

        selected_befund = models.WrightsTestHyperabduktionSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "edens_test":

        selected_befund = models.EdensTestCostoclavikulaererDruckSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "east_test":

        selected_befund = models.ElevatedArmStressTestEASTSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "cyrax_release_test":

        selected_befund = models.CyraxReleaseTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "morley_compression_test":

        selected_befund = models.MorleyCmpressionTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "irritierbarkeit_schulter_star":

        selected_befund = (
            models.IrritierbarkeitderSchulterAnlehnungSTASchulterDiagnose.objects.get(
                id=befundId
            )
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "alltagsfunktionen_schulter":

        selected_befund = models.AlltagsfunktionenSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "umfangsmessung_arm":

        selected_befund = models.UmfangsmessungArm.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "scapula_assistenstest_sat":

        selected_befund = models.ScapulaAssistenstesSATSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "lateral_scapula_slide_test":

        selected_befund = models.LateralerScapulaSlideTestSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "scapula_retraction_test_srt":

        selected_befund = models.ScapulaRetractionTestSRTSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "lateraler_scapula_slide_test":

        selected_befund = models.LateralerScapulaSlideTestSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "jobe_test":

        selected_befund = models.JobeTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "null_grad_adduktionstest":

        selected_befund = models.NullGradAdduktionstestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "drop_arm_zeichen":

        selected_befund = models.DropArmZeichenSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "lift_off_test":

        selected_befund = models.LiftOffTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "belly_press_belly_off_zeichen":

        selected_befund = models.BellyPressBellyOffZeichenSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "bear_hug_test":

        selected_befund = models.BearHugTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "null_grad_aussenrotationstest":

        selected_befund = models.NullGradAußenrotationstestSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "painful_arc":

        selected_befund = models.PainfulArcSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "hawkins_kennedy_test":

        selected_befund = models.HawkinsKennedyTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "neer_test":

        selected_befund = models.NeerTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "unspezifischer_bicepssehenen_test":

        selected_befund = models.UnspezifischerBicepssehenenTestSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "yergason":

        selected_befund = models.YergasonSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "speedys_test":

        selected_befund = models.SpeedysTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "o_briens_test":

        selected_befund = models.OBriensTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "biceps_load_test":

        selected_befund = models.BicepsLoadTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "supine_flexion_resitance_test":

        selected_befund = models.SupineFlexionResitanceTestSchulter.objects.get(
            id=befundId
        )

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    if befund == "crank_test":

        selected_befund = models.CrankTestSchulter.objects.get(id=befundId)

        if request.user == selected_befund.created_by:

            selected_befund.delete()

    return HttpResponse("Updated Succesfully")
