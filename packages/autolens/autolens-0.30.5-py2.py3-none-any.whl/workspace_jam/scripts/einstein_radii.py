from autolens.model.profiles import mass_profiles as mp

sie = al.mass_profiles.EllipticalIsothermalKormann(einstein_radius=2.0, axis_ratio=0.5)

print(sie.einstein_radius_in_units())
