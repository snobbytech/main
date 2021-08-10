// A set of css styles that we can share
// between our components.
// Doing it this way until we finda  better abstraction.

const universal_styles = {
  dottedButton: {
    width: "100%",
    justifyContent: "center",
    textTransform: "none",
    letterSpacing: "-.012em",
    fontSize: "1rem",
    borderRadius: "5px",
    boxShadow: "none",
    height: "48px!important",
    background: "white",
  },
  submitButton: {
    width: "50%",
    justifyContent: "center",
    textTransform: "none",
    letterSpacing: "-.012em",
    fontSize: "1rem",
    borderRadius: "5px",
    boxShadow: "none",
    // borderStyle: "dashed",
    height: "48px!important",
    background: "white",
  },
  onboardingLabels: { fontWeight: "bold", fontSize: "20px" },
};

export default universal_styles;
