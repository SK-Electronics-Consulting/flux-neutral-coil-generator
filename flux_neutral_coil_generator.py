import pcbnew
import FootprintWizardBase


class FluxNeutralCoilGen(FootprintWizardBase.FootprintWizard):
    GetName = lambda self: 'Flux Neutral Coil Generator'
    GetDescription = lambda self: 'Generates a flux-neutral coil within a circular aperture.'
    GetValue = lambda self: 'temporary_name'

    def GenerateParameterList(self):
        self.AddParam("Installation Information", "Outer Ring diameter", self.uMM, 150)
        self.AddParam("Fab Specs", "trace_width", self.uMM, 0.2)
        self.AddParam("Fab Specs", "trace_spacing", self.uMM, 0.2)
        self.AddParam("Coil specs", "turns", self.uInteger, 10)

        # pass

    def CheckParameters(self):
        self.trace_width = self.parameters['Fab Specs']['trace_width']

        # pass

    def BuildThisFootprint(self):
        t_size = self.GetTextSize()


