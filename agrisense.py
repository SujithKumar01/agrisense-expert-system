"""
AgriSense - Rule-Based Expert System for Crop Disease & Fertilizer Recommendation
Requires: experta  (pip install experta)

This is a self-contained example engine with:
- Facts for Crop, Soil, Symptoms, Weather, Lab (NPK, pH), PestPresence
- Rules for diagnosing common issues and recommending fertilizers/treatments
- Example facts and demo run()

Note: This system is advisory and simplified. Use local agronomist/lab results for final decisions.
"""

from experta import *

# -------------------------
# Fact definitions
# -------------------------
class Crop(Fact):
    """Crop(name='tomato', stage='vegetative'|'flowering'|'fruiting')"""
    pass

class Soil(Fact):
    """Soil(type='clay'|'sandy'|'loam', moisture='low'|'adequate'|'high', ph=float)"""
    pass

class Lab(Fact):
    """Lab(N=ppm, P=ppm, K=ppm, ph=float). Units simplified."""
    pass

class Symptoms(Fact):
    """Symptoms(leaf_spots=True, yellowing=True, wilting=True, stem_lesions=True,
                mosaic=True, powdery_white=True, black_sooty=True)"""
    pass

class Weather(Fact):
    """Weather(temp=float (C), humidity=int (pct), recent_rain_days=int)"""
    pass

class PestPresence(Fact):
    """PestPresence(aphids=True, mites=True, caterpillars=True, whiteflies=True)"""
    pass

class Diagnosis(Fact):
    """Holds a diagnosis result"""
    pass

class Recommendation(Fact):
    """Holds a fertilizer/treatment recommendation"""
    pass

# -------------------------
# Helper functions
# -------------------------
def interpret_npk(N, P, K):
    """Return qualitative levels for simple thresholding (very simplified)."""
    # thresholds are illustrative — adapt to real lab ranges & crop needs
    def level(x):
        if x < 50:
            return 'low'
        elif x < 150:
            return 'medium'
        else:
            return 'high'
    return level(N), level(P), level(K)

# -------------------------
# The Expert Engine
# -------------------------
class AgriSenseEngine(KnowledgeEngine):
    # Prioritize diagnosis rules (higher salience) over fertilizer rules (lower)
    @Rule(Symptoms(leaf_spots=True, powdery_white=True))
    def powdery_mildew(self):
        self.declare(Diagnosis(disease='Powdery Mildew',
                               confidence=0.8,
                               notes='Look for white powder on leaf surfaces'))
        self.declare(Recommendation(treatment='Apply fungicide targeting powdery mildew; improve air circulation; remove heavily infected leaves'))

    @Rule(Symptoms(leaf_spots=True, stem_lesions=True),
          Weather(humidity=P(lambda h: h > 75)))
    def blight_like(self):
        self.declare(Diagnosis(disease='Blight-like infection (possible bacterial/fungal)',
                               confidence=0.85,
                               notes='Leaf spots + stem lesions; wet humid weather favors blights'))
        self.declare(Recommendation(treatment='Use appropriate bactericide/fungicide; remove infected material; avoid overhead irrigation'))

    @Rule(Symptoms(mosaic=True))
    def viral_mosaic(self):
        self.declare(Diagnosis(disease='Viral Mosaic',
                               confidence=0.9,
                               notes='Mosaic patterns on leaves often indicate virus; vector control important'))
        self.declare(Recommendation(treatment='No chemical cure for virus; rogue and destroy infected plants; control aphids/whiteflies'))

    @Rule(Symptoms(wilting=True),
          PestPresence(caterpillars=True))
    def insect_damage_wilt(self):
        self.declare(Diagnosis(disease='Insect damage (larval feeding)',
                               confidence=0.75,
                               notes='Wilting with caterpillars suggests stem/root boring or heavy defoliation'))
        self.declare(Recommendation(treatment='Inspect for larvae; use biological control (Bt) or targeted insecticide; remove affected parts'))

    @Rule(Symptoms(yellowing=True),
          Lab(N=P(lambda n: n < 50)))
    def nitrogen_deficiency_symptom(self):
        self.declare(Diagnosis(disease='Nutrient deficiency - Nitrogen',
                               confidence=0.8,
                               notes='Yellowing, especially older leaves, suggests N deficiency'))
        self.declare(Recommendation(treatment='Top-dress with nitrogenous fertilizer (e.g., urea) as per crop need; split applications'))

    @Rule(AS.lab << Lab(N=MATCH.N, P=MATCH.P, K=MATCH.K))
    def fertilizer_npk_evaluation(self, lab, N, P, K):
        """Generic fertilizer recommendation based on lab values and an optional crop fact."""
        Nlvl, Plvl, Klvl = interpret_npk(N, P, K)
        recs = []
        if Nlvl == 'low':
            recs.append('Apply nitrogen fertilizer (e.g., Urea or CAN) - consider split dosing')
        if Plvl == 'low':
            recs.append('Apply phosphorus fertilizer (e.g., Single Super Phosphate) at planting or as recommended')
        if Klvl == 'low':
            recs.append('Apply potassium fertilizer (e.g., MOP) to boost fruiting/stress tolerance')
        if not recs:
            recs.append('Soil NPK levels are adequate; maintain balanced fertilization and monitor')
        self.declare(Recommendation(fertilizer_recommendations=recs))

    @Rule(AS.crop << Crop(name=MATCH.name, stage=MATCH.stage),
          Lab(N=MATCH.N, P=MATCH.P, K=MATCH.K))
    def crop_stage_specific(self, crop, name, stage, N, P, K):
        """Refine N requirement by crop stage (illustrative guidance)."""
        # Simplified: vegetative needs more N; flowering/fruiting needs K
        advice = []
        Nlvl, Plvl, Klvl = interpret_npk(N, P, K)
        if stage == 'vegetative' and Nlvl == 'low':
            advice.append('Increase nitrogen to support vegetative growth (split applications)')
        if stage in ('flowering', 'fruiting') and Klvl == 'low':
            advice.append('Increase potassium to support flowering/fruition')
        if advice:
            self.declare(Recommendation(stage_advice=advice))

    @Rule(AS.soil << Soil(type=MATCH.stype, ph=MATCH.ph),
          TEST(lambda ph: ph is not None and (ph < 5.5 or ph > 7.8)))
    def soil_ph_issue(self, soil, stype, ph):
        """Detect extreme soil pH issues and suggest adjustment."""
        if ph < 5.5:
            note = 'Soil is acidic (pH={:.2f}). Consider liming to raise pH.'.format(ph)
        else:
            note = 'Soil is alkaline (pH={:.2f}). Consider sulfur or acidifying amendments.'.format(ph)
        self.declare(Recommendation(soil_ph_note=note))

    @Rule(PestPresence(aphids=True) | PestPresence(whiteflies=True))
    def vector_warning(self):
        """Vector-borne disease prevention rule."""
        self.declare(Recommendation(treatment='Vectors detected: control aphids/whiteflies using IPM (neem/biocontrol/soft insecticides); use reflective mulches or yellow sticky traps'))
        self.declare(Diagnosis(disease='High vector presence - risk of viral spread', confidence=0.7))

    @Rule(AND(NOT(Diagnosis()), NOT(Recommendation())))
    def no_data(self):
        """Fallback if no diagnosis or recommendations were produced."""
        self.declare(Recommendation(general='Insufficient symptom/lab data to provide a targeted recommendation. Collect more info: detailed symptoms, lab NPK, recent weather.'))

    # Optional: collect and print results as they are declared
    def get_results(self):
        diagnoses = [f for f in self.facts.values() if isinstance(f, Diagnosis)]
        recs = [f for f in self.facts.values() if isinstance(f, Recommendation)]
        return diagnoses, recs

# -------------------------
# Demo / Example usage
# -------------------------
def main():
    engine = AgriSenseEngine()
    engine.reset()

    # Example: Tomato plant with powdery white on leaves, high humidity, low NPK
    engine.declare(Crop(name='tomato', stage='flowering'))
    engine.declare(Soil(type='loam', moisture='adequate', ph=6.3))
    engine.declare(Lab(N=30, P=40, K=45, ph=6.3))  # low N,P,K by our simple thresholds
    engine.declare(Symptoms(leaf_spots=True, powdery_white=True, yellowing=False, wilting=False))
    engine.declare(Weather(temp=22.0, humidity=85, recent_rain_days=5))
    engine.declare(PestPresence(aphids=False, whiteflies=False, caterpillars=False))

    engine.run()  # run rules

    diagnoses, recs = engine.get_results()
    print("\n--- Diagnoses ---")
    for d in diagnoses:
        # d is a Fact object with slots like disease, confidence, notes
        print({k: v for k, v in d.items() if k != '__factid__'})

    print("\n--- Recommendations ---")
    for r in recs:
        print({k: v for k, v in r.items() if k != '__factid__'})

if __name__ == '__main__':
    main()
