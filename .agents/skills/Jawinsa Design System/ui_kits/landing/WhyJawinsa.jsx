/* global React */
const { useEffect, useRef, useState } = React;

const PILLARS = [
  {
    icon: "shield-check",
    title: "Equipo certificado",
    desc: "Técnicos con certificación multimarca y herramientas de diagnóstico OBD-II actualizadas.",
  },
  {
    icon: "gauge-circle",
    title: "Diagnóstico antes de cotizar",
    desc: "No reparamos a ciegas. Diagnóstico electrónico documentado y cotización detallada.",
  },
  {
    icon: "badge-check",
    title: "Experiencia B2B comprobada",
    desc: "Contratos con flotas de logística, construcción y operadores. Postulamos a licitaciones.",
  },
];

function WhyJawinsa() {
  const ref = useRef(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    if (!ref.current) return;
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) { setInView(true); io.disconnect(); }
    }, { threshold: 0.15 });
    io.observe(ref.current);
    return () => io.disconnect();
  }, []);

  return (
    <section id="nosotros" className="section" ref={ref}>
      <div className="container">
        <div className={`reveal ${inView ? "in" : ""}`}>
          {/* Big dark feature panel */}
          <div style={{
            background: "var(--ink)",
            color: "var(--paper)",
            borderRadius: 32,
            padding: "clamp(40px, 5vw, 72px)",
            position: "relative",
            overflow: "hidden",
            boxShadow: "var(--shadow-3)",
          }}>
            {/* ambient amber blob */}
            <div style={{
              position: "absolute",
              right: -120, top: -120,
              width: 500, height: 500,
              background: "radial-gradient(circle, rgba(232,115,44,0.25), transparent 65%)",
              pointerEvents: "none",
            }} />
            {/* big J */}
            <div style={{
              position: "absolute",
              left: "-2%", bottom: "-30%",
              fontFamily: "var(--font-display)",
              fontWeight: 900,
              fontSize: 600,
              lineHeight: 1,
              color: "rgba(246,244,240,0.04)",
              letterSpacing: "-0.05em",
              pointerEvents: "none",
              userSelect: "none",
            }}>J</div>

            <div style={{ position: "relative", zIndex: 1, display: "grid", gridTemplateColumns: "1.1fr 1fr", gap: 48, alignItems: "end" }} className="why-head">
              <div>
                <div className="eyebrow" style={{ color: "var(--steel-400)" }}>
                  <span className="dot"></span>Por qué Jawinsa
                </div>
                <h2 style={{
                  fontFamily: "var(--font-display)",
                  fontWeight: 800,
                  fontSize: "clamp(36px, 4.5vw, 64px)",
                  lineHeight: 1.02,
                  letterSpacing: "-0.03em",
                  margin: "16px 0 0",
                  color: "var(--paper)",
                  textWrap: "balance",
                }}>
                  Confianza técnica,<br/>no promesas de marketing.
                </h2>
              </div>
              <p style={{
                fontFamily: "var(--font-body)",
                fontSize: 17,
                lineHeight: 1.55,
                color: "var(--steel-300)",
                margin: 0,
                maxWidth: 460,
                justifySelf: "end",
              }}>
                Operamos con la disciplina de una flota industrial y la atención de
                un taller de barrio. Nuestros clientes vuelven porque devolvemos la
                unidad operativa, a tiempo y bien documentada.
              </p>
            </div>

            {/* Pillars row */}
            <div className="why-pillars" style={{
              marginTop: 64,
              position: "relative", zIndex: 1,
              display: "grid",
              gridTemplateColumns: "repeat(3, 1fr)",
              gap: 14,
            }}>
              {PILLARS.map((p, i) => <Pillar key={p.title} {...p} index={i} />)}
            </div>

            {/* Brand strip */}
            <div className="why-brands" style={{
              marginTop: 72,
              position: "relative", zIndex: 1,
              padding: "28px 0",
              borderTop: "1px solid rgba(246,244,240,0.08)",
              display: "grid",
              gridTemplateColumns: "auto 1fr",
              gap: 32,
              alignItems: "center",
            }}>
              <div style={{
                fontFamily: "var(--font-body)",
                fontSize: 11,
                fontWeight: 700,
                letterSpacing: "0.22em",
                textTransform: "uppercase",
                color: "var(--steel-400)",
                maxWidth: 180,
              }}>Marcas con las que trabajamos</div>

              <div style={{
                display: "flex",
                gap: 40,
                flexWrap: "wrap",
                alignItems: "center",
                opacity: 0.85,
              }}>
                {["TOYOTA", "HYUNDAI", "VOLVO", "CATERPILLAR", "CUMMINS", "PERKINS", "KOMATSU"].map(b => (
                  <div key={b} style={{
                    fontFamily: "var(--font-display)",
                    fontWeight: 800,
                    fontSize: 16,
                    letterSpacing: "0.14em",
                    color: "var(--steel-400)",
                  }}>{b}</div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @media (max-width: 900px) {
          .why-head { grid-template-columns: 1fr !important; gap: 16px !important; }
          .why-head p { justify-self: start !important; }
          .why-pillars { grid-template-columns: 1fr !important; }
          .why-brands { grid-template-columns: 1fr !important; gap: 20px !important; }
        }
      `}</style>
    </section>
  );
}

function Pillar({ icon, title, desc, index }) {
  return (
    <div style={{
      background: "rgba(246,244,240,0.04)",
      border: "1px solid rgba(246,244,240,0.08)",
      borderRadius: 22,
      padding: "28px 24px",
      display: "flex",
      flexDirection: "column",
      gap: 14,
    }}>
      <div style={{
        width: 44, height: 44,
        borderRadius: 14,
        background: "var(--accent)",
        color: "#fff",
        display: "flex", alignItems: "center", justifyContent: "center",
      }}>
        <i data-lucide={icon} width="22" height="22" {...{"stroke-width":"1.75"}}></i>
      </div>
      <h3 style={{
        fontFamily: "var(--font-display)",
        fontWeight: 700,
        fontSize: 22,
        lineHeight: 1.15,
        letterSpacing: "-0.02em",
        color: "var(--paper)",
        margin: 0,
      }}>{title}</h3>
      <p style={{
        fontFamily: "var(--font-body)",
        fontSize: 14,
        lineHeight: 1.55,
        color: "var(--steel-300)",
        margin: 0,
      }}>{desc}</p>
    </div>
  );
}

window.WhyJawinsa = WhyJawinsa;
