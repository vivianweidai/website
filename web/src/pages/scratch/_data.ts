// SCRATCH — shared mock data for the /projects redesign options.
// Not routed (underscore prefix). Delete with the rest of src/pages/scratch/.
//
// Everything here is REAL: real toy names from technology.yml, real photo
// paths from web/public/research/. Only the `status`, `note` and `date`
// fields are invented, to show what each layout would look like populated.

const enc = (s: string) => s.split('/').map(encodeURIComponent).join('/');

/** Photo under web/public/research/projects/<proj>/<rest> */
export const P = (proj: string, rest: string) =>
  '/research/projects/' + enc(proj + '/' + rest);
/** Tech hero under web/public/research/technology/<sci>/<tech>/<file> */
export const T = (sci: string, tech: string, file: string) =>
  '/research/technology/' + enc(sci + '/' + tech + '/' + file);

export type Sci = 'phys' | 'chem' | 'bio' | 'astro' | 'math' | 'comp';

export const SCI: Record<Sci, { name: string; abbr: string; tint: string; ink: string }> = {
  phys:  { name: 'Physics',     abbr: 'Phys',  tint: 'var(--subj-phys)',  ink: '#ea580c' },
  chem:  { name: 'Chemistry',   abbr: 'Chem',  tint: 'var(--subj-chem)',  ink: '#5c7a10' },
  bio:   { name: 'Biology',     abbr: 'Bio',   tint: 'var(--subj-bio)',   ink: '#0e8577' },
  astro: { name: 'Astronomy',   abbr: 'Astro', tint: 'var(--subj-astro)', ink: '#e11d48' },
  math:  { name: 'Mathematics', abbr: 'Math',  tint: 'var(--subj-math)',  ink: '#2563eb' },
  comp:  { name: 'Computing',   abbr: 'Comp',  tint: 'var(--subj-comp)',  ink: '#7c3aed' },
};

export type Status = 'boxed' | 'working' | 'measured' | 'extended';
export const STATUS: Record<Status, { label: string; blurb: string }> = {
  boxed:    { label: 'Unboxed',  blurb: 'in the house, not yet switched on' },
  working:  { label: 'Working',  blurb: 'it does the thing it says on the box' },
  measured: { label: 'Measured', blurb: 'got a number we could check against a known answer' },
  extended: { label: 'Extended', blurb: 'pointed at something nobody handed us the answer to' },
};

export interface Toy {
  name: string;
  short: string;
  sci: Sci;
  /** bench = you can put your hands on it. desk = you look it up or run it. */
  kind: 'bench' | 'desk';
  note: string;
  status: Status;
  img?: string;
  shots?: number;
}

// ── Photo shorthands ────────────────────────────────────────────────
const STAR = (f: string) => P('20260725 Stargazing', 'data/' + f);
const CELL = (f: string) => P('20260725 Cellgazing', 'data/' + f);
const UVVIS = (f: string) => P('20260420 UV-Vis Spectroscopy', f);
const IR = (f: string) => P('20260419 IR Spectroscopy', f);
const CENT = (f: string) => P('20260411 Centrifuge', f);
const MELT = (f: string) => P('20260405 Melting Point', f);
const PROBE = (f: string) => P('20260404 Four Point Probe', f);
const CAT = (f: string) => P('20250225 Catfood', f);
const GENES = P('20260401 Genes in Space', 'photos/photo.jpeg');

export const TOYS: Toy[] = [
  // ── PHYSICS ───────────────────────────────────────────────────────
  { name: 'Digilent Analog Discovery 3', short: 'Oscilloscope', sci: 'phys', kind: 'bench',
    note: 'Scope + generator on USB', status: 'extended', img: T('physics', 'Engineering', 'circuits.jpeg'), shots: 14 },
  { name: 'Prusa CORE One+', short: '3D Printer', sci: 'phys', kind: 'bench',
    note: 'Make the fixture that holds the thing', status: 'measured', img: PROBE('photos/samples/samples2.jpeg'), shots: 9 },
  { name: 'LEGO Education SPIKE Prime Set', short: 'LEGO', sci: 'phys', kind: 'bench',
    note: 'Motion you can rebuild in ten minutes', status: 'working', img: T('physics', 'Mechanics', 'mechanics.jpeg'), shots: 4 },
  { name: 'Vernier Go Direct Force and Acceleration Sensor', short: 'Force', sci: 'phys', kind: 'bench',
    note: 'Push, pull, jerk', status: 'measured', img: T('physics', 'Mechanics', 'mechanics.jpeg'), shots: 6 },
  { name: 'Vernier Go Direct Motion Detector', short: 'Motion', sci: 'phys', kind: 'bench',
    note: 'Distance by echo', status: 'working', img: T('physics', 'Mechanics', 'mechanics.jpeg'), shots: 3 },
  { name: 'Vernier Go Direct Photogate', short: 'Time', sci: 'phys', kind: 'bench',
    note: 'The beam breaks, the clock runs', status: 'measured', img: T('physics', 'Mechanics', 'mechanics.jpeg'), shots: 5 },
  { name: 'Vernier Go Direct Gas Pressure Sensor', short: 'Pressure', sci: 'phys', kind: 'bench',
    note: 'Sealed syringe, squeezed', status: 'working', img: T('physics', 'Thermodynamics', 'thermodynamics.jpeg'), shots: 2 },
  { name: 'Vernier Go Direct Turbidity', short: 'Turbidity', sci: 'phys', kind: 'bench',
    note: 'How cloudy is cloudy', status: 'boxed', img: T('physics', 'Thermodynamics', 'thermodynamics.jpeg'), shots: 0 },
  { name: 'Vernier Go Direct 3-Axis Magnetic Field Sensor', short: 'Magnetism', sci: 'phys', kind: 'bench',
    note: 'Hall probe, three ways', status: 'working', img: T('physics', 'Electromagnetism', 'electromagnetism.jpeg'), shots: 3 },
  { name: 'Vernier Spectrophotometer Optical Fiber', short: 'Optical Fiber', sci: 'phys', kind: 'bench',
    note: 'Spectra outside the cuvette', status: 'boxed', img: T('chemistry', 'Spectroscopy', 'spectroscopy.jpeg'), shots: 1 },

  // ── CHEMISTRY ─────────────────────────────────────────────────────
  { name: 'Vernier Go Direct Fluorescence UV-VIS Spectrophotometer', short: 'UV-Vis', sci: 'chem', kind: 'bench',
    note: 'Colour, as a curve', status: 'extended', img: UVVIS('photos/samples/samples3.jpeg'), shots: 27 },
  { name: 'Vernier Go Direct pH Sensor', short: 'pH', sci: 'chem', kind: 'bench',
    note: 'One ion, no current', status: 'measured', img: T('chemistry', 'Electrochemistry', 'electrochemistry.jpeg'), shots: 7 },
  { name: 'Vernier Go Direct Conductivity Probe', short: 'Conductivity', sci: 'chem', kind: 'bench',
    note: 'All the ions at once', status: 'working', img: T('chemistry', 'Electrochemistry', 'electrochemistry.jpeg'), shots: 4 },
  { name: 'Vernier Go Direct Polarimeter', short: 'Polarimeter', sci: 'chem', kind: 'bench',
    note: 'Which way the sugar turns light', status: 'boxed', img: T('chemistry', 'Spectroscopy', 'spectroscopy.jpeg'), shots: 0 },
  { name: 'Vernier Go Direct Temperature Probe', short: 'Temperature', sci: 'chem', kind: 'bench',
    note: 'The one that goes in everything', status: 'measured', img: MELT('photos/setup/setup2.jpeg'), shots: 11 },

  // ── BIOLOGY ───────────────────────────────────────────────────────
  { name: 'Swift Optical SW380T Trinocular Compound Microscope', short: 'Compound', sci: 'bio', kind: 'bench',
    note: 'Down to the cell', status: 'extended', img: CELL('tissue-section.jpg'), shots: 22 },
  { name: 'AmScope SM-4TZ-144 Trinocular Stereo Microscope', short: 'Stereo', sci: 'bio', kind: 'bench',
    note: 'Two eyes, real depth', status: 'measured', img: CELL('leaf-epidermis.jpg'), shots: 12 },
  { name: 'Dino-Lite AF4515T-FUW Digital Microscope', short: 'Surface', sci: 'bio', kind: 'bench',
    note: 'Handheld, points anywhere', status: 'measured', img: CELL('reticulate-specimen.jpg'), shots: 8 },
  { name: 'miniPCR mini16 Thermal Cycler', short: 'PCR', sci: 'bio', kind: 'bench',
    note: 'Copy the gene until you can see it', status: 'working', img: CENT('photos/setup/setup1.jpeg'), shots: 6 },
  { name: 'GELATO Electrophoresis and Visualization System', short: 'Electrophoresis', sci: 'bio', kind: 'bench',
    note: 'Sort by size, look with blue light', status: 'working', img: CENT('photos/samples/samples5.jpeg'), shots: 5 },
  { name: 'P51 Molecular Fluorescence Viewer', short: 'Fluorescence', sci: 'bio', kind: 'bench',
    note: 'Glow box', status: 'boxed', img: T('biology', 'Genomics', 'genomics.jpeg'), shots: 1 },
  { name: 'Vernier Go Direct EKG Sensor', short: 'EKG', sci: 'bio', kind: 'bench',
    note: 'Your own heart, on a trace', status: 'measured', img: T('biology', 'Physiology', 'physiology.jpeg'), shots: 9 },
  { name: 'Vernier Go Direct Spirometer', short: 'Spirometer', sci: 'bio', kind: 'bench',
    note: 'Breathe in, breathe out', status: 'working', img: T('biology', 'Physiology', 'physiology.jpeg'), shots: 3 },
  { name: 'Vernier Go Direct O2 + CO2 Gas Sensor Bundle', short: 'Respiration', sci: 'bio', kind: 'bench',
    note: 'What went in vs. what came out', status: 'boxed', img: T('biology', 'Physiology', 'physiology.jpeg'), shots: 0 },

  // ── ASTRONOMY ─────────────────────────────────────────────────────
  { name: 'ZWO Seestar S30 Pro with Tilting Wedge', short: 'Optical', sci: 'astro', kind: 'bench',
    note: 'The one telescope we own', status: 'extended', img: STAR('M_31__Stacked_25_M_31_20.0s_IRCUT_20260730-015655.jpg'), shots: 41 },
  { name: 'UBC Thunderbird South Observatory', short: 'Earth', sci: 'astro', kind: 'desk',
    note: 'Somebody else’s big mirror, over the network', status: 'working', img: STAR('NGC_7000__Stacked_20_NGC_7000_20.0s_IRCUT_20260730-014616.jpg'), shots: 2 },
  { name: 'MAST Portal', short: 'Space', sci: 'astro', kind: 'desk', note: 'Space telescope archive', status: 'working' },
  { name: 'Gaia Archive', short: 'Astrometry', sci: 'astro', kind: 'desk', note: 'A billion positions', status: 'measured' },
  { name: 'AAVSO Database', short: 'Photometry', sci: 'astro', kind: 'desk', note: 'Brightness over time', status: 'measured' },
  { name: 'SIMBAD', short: 'Stars', sci: 'astro', kind: 'desk', note: 'What is that thing called', status: 'extended' },
  { name: 'Pickles Stellar Atlas', short: 'Spectroscopy', sci: 'astro', kind: 'desk', note: 'Reference spectra to match against', status: 'working' },
  { name: 'Transient Name Server', short: 'Transients', sci: 'astro', kind: 'desk', note: 'What just went bang', status: 'boxed' },
  { name: 'Galaxy Zoo', short: 'Galaxies', sci: 'astro', kind: 'desk', note: 'Morphology references', status: 'boxed' },

  // ── MATHEMATICS (all desk) ────────────────────────────────────────
  { name: 'NumPy', short: 'NumPy', sci: 'math', kind: 'desk', note: 'Arrays and linear algebra', status: 'extended' },
  { name: 'SciPy', short: 'SciPy', sci: 'math', kind: 'desk', note: 'Fits, transforms, tests', status: 'extended' },
  { name: 'Matplotlib', short: 'Matplotlib', sci: 'math', kind: 'desk', note: 'Everything gets plotted', status: 'extended' },
  { name: 'Wolfram', short: 'Wolfram', sci: 'math', kind: 'desk', note: 'When the algebra is the hard part', status: 'measured' },
  { name: 'LaTeX', short: 'LaTeX', sci: 'math', kind: 'desk', note: 'Typesetting', status: 'measured' },

  // ── COMPUTING (all desk) ──────────────────────────────────────────
  { name: 'Jupyter', short: 'Jupyter', sci: 'comp', kind: 'desk', note: 'Where the messing-around gets saved', status: 'extended' },
  { name: 'GitHub', short: 'GitHub', sci: 'comp', kind: 'desk', note: 'Version control and hosting', status: 'extended' },
  { name: 'scikit-learn', short: 'scikit-learn', sci: 'comp', kind: 'desk', note: 'Classify and regress', status: 'measured' },
  { name: 'PyTorch', short: 'PyTorch', sci: 'comp', kind: 'desk', note: 'When the model needs gradients', status: 'working' },
  { name: 'Docker', short: 'Docker', sci: 'comp', kind: 'desk', note: 'So it runs on the other machine too', status: 'working' },
  { name: 'Zenodo', short: 'Zenodo', sci: 'comp', kind: 'desk', note: 'DOI for a dataset', status: 'boxed' },
];

export const BENCH = TOYS.filter((t) => t.kind === 'bench');
export const DESK = TOYS.filter((t) => t.kind === 'desk');

// ── The photo stream ────────────────────────────────────────────────
export interface Shot {
  src: string;
  cap: string;
  toy: string;   // short label
  sci: Sci;
  date: string;  // display date
  tall?: boolean;
  video?: boolean;
}

export const STREAM: Shot[] = [
  { src: STAR('M_31__Stacked_25_M_31_20.0s_IRCUT_20260730-015655.jpg'), cap: 'M 31 — 25 × 20s', toy: 'Seestar', sci: 'astro', date: 'Jul 30', tall: true },
  { src: STAR('NGC_7000__Stacked_20_NGC_7000_20.0s_IRCUT_20260730-014616.jpg'), cap: 'NGC 7000 field — 20 × 20s', toy: 'Seestar', sci: 'astro', date: 'Jul 30', tall: true },
  { src: STAR('Albireo__Light_Albireo_20.0s_IRCUT_failed_20260729-225851.jpg'), cap: 'Albireo — a whole field of spectra, by accident', toy: 'Seestar', sci: 'astro', date: 'Jul 29', tall: true },
  { src: STAR('Vega__Light_Vega_5.0s_IRCUT_failed_20260729-222828.jpg'), cap: 'Vega spectrum — the grating is on backwards', toy: 'Seestar', sci: 'astro', date: 'Jul 29', tall: true },
  { src: STAR('Juno__Light_Juno_20.0s_IRCUT_20260729-003012.jpg'), cap: 'Juno — after (it moved)', toy: 'Seestar', sci: 'astro', date: 'Jul 29', tall: true },
  { src: STAR('Juno__Light_Juno_20.0s_IRCUT_20260729-000521.jpg'), cap: 'Juno — before', toy: 'Seestar', sci: 'astro', date: 'Jul 29', tall: true },
  { src: STAR('M_13__Stacked_5_M_13_60.0s_IRCUT_20260728-225801.jpg'), cap: 'M 13 — 5 × 60s', toy: 'Seestar', sci: 'astro', date: 'Jul 28', tall: true },
  { src: STAR('Delta_Cygni__Stacked_54_Delta_Cygni_5.0s_IRCUT_20260728-223243.jpg'), cap: 'Delta Cygni — 54 × 5s', toy: 'Seestar', sci: 'astro', date: 'Jul 28', tall: true },
  { src: CELL('tissue-section.jpg'), cap: 'Tissue section, 400×', toy: 'Compound', sci: 'bio', date: 'Jul 25' },
  { src: CELL('leaf-epidermis.jpg'), cap: 'Leaf epidermis — stomata everywhere', toy: 'Stereo', sci: 'bio', date: 'Jul 25' },
  { src: CELL('reticulate-specimen.jpg'), cap: 'Reticulate specimen, handheld', toy: 'Surface', sci: 'bio', date: 'Jul 25' },
  { src: STAR('Vega__Stacked_8_Vega_10.0s_IRCUT_20260725-011926.jpg'), cap: 'Vega — 8 × 10s', toy: 'Seestar', sci: 'astro', date: 'Jul 25', tall: true },
  { src: STAR('RR_Lyrae__Stacked_21_RR_Lyrae_5.0s_IRCUT_20260725-020642.jpg'), cap: 'RR Lyrae — 21 × 5s', toy: 'Seestar', sci: 'astro', date: 'Jul 25', tall: true },
  { src: UVVIS('photos/samples/samples3.jpeg'), cap: 'The amber bottle shelf', toy: 'UV-Vis', sci: 'chem', date: 'Apr 20' },
  { src: UVVIS('photos/samples/samples5.jpeg'), cap: 'Cuvettes loaded', toy: 'UV-Vis', sci: 'chem', date: 'Apr 20' },
  { src: UVVIS('photos/samples/samples6.jpeg'), cap: 'Quinine under the lamp', toy: 'UV-Vis', sci: 'chem', date: 'Apr 20' },
  { src: UVVIS('output/images/uvvis_overlay.png'), cap: 'All four traces on one axis', toy: 'UV-Vis', sci: 'chem', date: 'Apr 20' },
  { src: UVVIS('photos/setup/setup5.jpeg'), cap: 'Software fighting us again', toy: 'UV-Vis', sci: 'chem', date: 'Apr 20' },
  { src: IR('photos/samples/samples1.jpeg'), cap: 'Sample plate', toy: 'IR', sci: 'chem', date: 'Apr 19' },
  { src: IR('output/images/chem_oh_spectrum.png'), cap: 'That fat O–H band', toy: 'IR', sci: 'chem', date: 'Apr 19' },
  { src: CENT('photos/samples/samples1.jpeg'), cap: 'Red caps, ready to spin', toy: 'PCR', sci: 'bio', date: 'Apr 11' },
  { src: CENT('photos/samples/samples5.jpeg'), cap: 'Rack of everything', toy: 'Electrophoresis', sci: 'bio', date: 'Apr 11' },
  { src: CENT('photos/samples/samples11.jpeg'), cap: 'Blue caps this time', toy: 'PCR', sci: 'bio', date: 'Apr 11' },
  { src: CENT('photos/setup/setup3.jpeg'), cap: 'Weighing it out', toy: 'Temperature', sci: 'bio', date: 'Apr 11' },
  { src: MELT('photos/setup/setup5.jpeg'), cap: 'Watching the capillary go clear', toy: 'Temperature', sci: 'chem', date: 'Apr 5' },
  { src: MELT('photos/samples/samples1.jpeg'), cap: 'Capillaries, loaded', toy: 'Temperature', sci: 'chem', date: 'Apr 5' },
  { src: PROBE('photos/samples/samples1.jpeg'), cap: 'Coupons cut and laid out', toy: 'Oscilloscope', sci: 'phys', date: 'Apr 4' },
  { src: PROBE('photos/samples/samples3.jpeg'), cap: 'Gold on glass', toy: 'Oscilloscope', sci: 'phys', date: 'Apr 4' },
  { src: PROBE('photos/setup/setup13.jpeg'), cap: 'Four probes down', toy: 'Oscilloscope', sci: 'phys', date: 'Apr 4' },
  { src: PROBE('output/mean_sheet_resistance.png'), cap: 'Sheet resistance, finally', toy: 'Matplotlib', sci: 'phys', date: 'Apr 4' },
  { src: GENES, cap: 'Our PCR run, on the ISS', toy: 'PCR', sci: 'bio', date: 'Apr 1' },
  { src: CAT('photos/setup/setup1.jpeg'), cap: 'The subject declines to participate', toy: 'SciPy', sci: 'bio', date: 'Feb 25' },
  { src: CAT('photos/setup/setup5.jpeg'), cap: 'Two bowls, blind trial', toy: 'SciPy', sci: 'bio', date: 'Feb 25' },
  { src: CAT('output/catfood_preference.png'), cap: 'She has a preference. p = 0.03', toy: 'SciPy', sci: 'comp', date: 'Feb 25' },
];

/** Chronological groups for the logbook layout. */
export const SESSIONS = [
  { date: 'July 30', sci: 'astro' as Sci, toy: 'Seestar', title: 'Andromeda, finally, at 20 seconds a frame',
    note: 'Clear enough to stack 25. The dust lane shows up without touching the stretch.',
    shots: [0, 1] },
  { date: 'July 29', sci: 'astro' as Sci, toy: 'Seestar', title: 'Grating night — mostly wrong, one accident worth keeping',
    note: 'Star Analyser mounted backwards for the first hour. The Albireo frame that came out of it has every star in the field smeared into its own spectrum, which is better than what we were aiming for.',
    shots: [2, 3] },
  { date: 'July 29', sci: 'astro' as Sci, toy: 'Seestar', title: 'Juno moved',
    note: 'Two frames, 25 minutes apart, same field. It moved. That is the whole result.',
    shots: [5, 4] },
  { date: 'July 25', sci: 'bio' as Sci, toy: 'Compound', title: 'Three scopes, same leaf',
    note: 'Handheld, stereo, compound — same specimen down the magnification ladder to see where each one gives up.',
    shots: [8, 9, 10] },
  { date: 'April 20', sci: 'chem' as Sci, toy: 'UV-Vis', title: 'Everything on the shelf that was coloured',
    note: 'Quinine fluoresces hard enough to see by eye under the lamp. Overlay at the end is four unrelated things that happen to share an axis.',
    shots: [13, 15, 16] },
  { date: 'April 11', sci: 'bio' as Sci, toy: 'PCR', title: 'Spin-down practice',
    note: 'No experiment. Just learning to balance the rotor and not crack a tube.',
    shots: [20, 21, 22] },
  { date: 'February 25', sci: 'bio' as Sci, toy: 'SciPy', title: 'The cat food trial',
    note: 'The first one. Two bowls, randomised, twenty trials. She has a preference and it is significant.',
    shots: [31, 32, 33] },
];

export const OPTIONS = [
  { slug: 'shelf',   n: 1, name: 'The Shelf',    thesis: 'The collection is the content. Toys first, science is a filter.' },
  { slug: 'logbook', n: 2, name: 'The Logbook',  thesis: 'Newest thing on top. A dated stream of nights and afternoons.' },
  { slug: 'benches', n: 3, name: 'Four Benches', thesis: 'Keep tabs, cut to four, demote math + computing to a toolchain rail.' },
  { slug: 'wall',    n: 4, name: 'The Wall',     thesis: 'No taxonomy at all. Every picture, one grid, filter pills.' },
  { slug: 'ladder',  n: 5, name: 'The Ladder',   thesis: 'Unboxed → Working → Measured → Extended. The moving pieces, as position.' },
];
