/* global React */
const { useEffect, useState, useRef } = React;

function ServiceLines() {
  return (
    <section id="servicios" className="section">
      <div className="container">
        <div className="sec-head" style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 32,
          alignItems: "end",
          marginBottom: 48,
        }}>
          <div>
            <div className="eyebrow"><span className="dot"></span>Líneas de servicio</div>
            <h2 style={{
              fontFamily: "var(--font-display)",
              fontWeight: 800,
              fontSize: "clamp(36px, 4.5vw, 64px)",
              lineHeight: 1.02,
              letterSpacing: "-0.03em",
              margin: "16px 0 0",
              textWrap: "balance",
              color: "var(--fg-1)",
            }}>
              Cuatro líneas.<br/>Una operación integral.
            </h2>
          </div>
          <p style={{
            fontFamily: "var(--font-body)",
            fontSize: 17,
            lineHeight: 1.55,
            color: "var(--fg-2)",
            margin: 0,
            maxWidth: 480,
            justifySelf: "end",
          }}>
            Atendemos desde un sedán particular hasta una flota de volquetes o un
            grupo electrógeno crítico — multimarca, con diagnóstico avanzado y
            repuestos en stock.
          </p>
        </div>

        {/* Bento grid */}
        <div className="bento" style={{
          display: "grid",
          gridTemplateColumns: "repeat(12, 1fr)",
          gridAutoRows: "minmax(220px, auto)",
          gap: 14,
        }}>
          {/* Auto — large feature */}
          <BentoCard
            span="span 7 / span 7"
            rowSpan="span 2"
            eyebrow="LÍNEA AUTOMOTRIZ"
            title="Autos & camionetas"
            desc="Mantenimiento preventivo y correctivo multimarca. Cambios de aceite, frenos, suspensión, transmisión y diagnóstico electrónico OBD-II."
            icon="car"
            chips={["Sedán", "SUV", "Pickup", "Híbrido"]}
            visual="large"
          />

          {/* Industrial — tall dark */}
          <BentoCard
            span="span 5 / span 5"
            rowSpan="span 2"
            eyebrow="LÍNEA INDUSTRIAL"
            title="Montacargas & gensets"
            desc="Especialistas en montacargas eléctricos y a combustión, y en grupos electrógenos Cummins, Perkins, Caterpillar."
            icon="forklift"
            chips={["Cummins", "Perkins", "Caterpillar"]}
            theme="dark"
            visual="industrial"
          />

          {/* Comercial — wide */}
          <BentoCard
            span="span 7 / span 7"
            eyebrow="LÍNEA COMERCIAL"
            title="Camiones & volquetes"
            desc="Servicio técnico para vehículos pesados de carga y construcción. Contratos de mantenimiento para flotas operativas."
            icon="truck"
            chips={["Camiones", "Volquetes", "Buses"]}
          />

          {/* Repuestos — accent */}
          <BentoCard
            span="span 5 / span 5"
            eyebrow="REPUESTOS"
            title="Repuestos & fluidos"
            desc="Venta directa de repuestos OEM y aftermarket, aceites y filtros."
            icon="cog"
            chips={["OEM", "Aceites", "Filtros"]}
            theme="accent"
          />
        </div>
      </div>

      <style>{`
        @media (max-width: 900px) {
          .sec-head { grid-template-columns: 1fr !important; gap: 16px !important; }
          .sec-head p { justify-self: start !important; }
          .bento { grid-template-columns: 1fr !important; }
          .bento > * { grid-column: span 1 / span 1 !important; grid-row: auto !important; }
        }
      `}</style>
    </section>
  );
}

function BentoCard({ span, rowSpan, eyebrow, title, desc, icon, chips, theme, visual }) {
  const ref = useRef(null);
  const [inView, setInView] = useState(false);
  const [hover, setHover] = useState(false);

  useEffect(() => {
    if (!ref.current) return;
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) { setInView(true); io.disconnect(); }
    }, { threshold: 0.1 });
    io.observe(ref.current);
    return () => io.disconnect();
  }, []);

  const dark = theme === "dark";
  const accent = theme === "accent";

  const bg = dark ? "var(--ink)" : accent ? "var(--accent)" : "var(--paper-elevated)";
  const fg = (dark || accent) ? "var(--paper)" : "var(--fg-1)";
  const sub = dark ? "var(--steel-300)" : accent ? "rgba(255,255,255,0.85)" : "var(--fg-2)";
  const eyebrowCol = dark ? "var(--steel-400)" : accent ? "rgba(255,255,255,0.7)" : "var(--fg-3)";

  return (
    <article
      ref={ref}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      className={`reveal ${inView ? "in" : ""}`}
      style={{
        gridColumn: span,
        gridRow: rowSpan,
        background: bg,
        color: fg,
        borderRadius: 28,
        border: dark || accent ? "1px solid transparent" : "1px solid rgba(14,16,20,0.05)",
        boxShadow: hover ? "var(--shadow-2)" : "var(--shadow-soft)",
        padding: visual === "large" ? "32px 36px 36px" : "26px 28px 30px",
        transition: "box-shadow var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out)",
        position: "relative",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        gap: 10,
        transform: hover ? "translateY(-2px)" : "translateY(0)",
        minHeight: 220,
      }}
    >
      {/* Icon */}
      <div style={{
        width: 44, height: 44,
        borderRadius: 14,
        background: dark || accent ? "rgba(255,255,255,0.12)" : "var(--ink)",
        color: dark || accent ? "#fff" : "var(--paper)",
        display: "flex", alignItems: "center", justifyContent: "center",
        flexShrink: 0,
      }}>
        <i data-lucide={icon} width="22" height="22" {...{"stroke-width":"1.75"}}></i>
      </div>

      <div style={{
        fontFamily: "var(--font-body)",
        fontSize: 11,
        fontWeight: 700,
        letterSpacing: "0.22em",
        textTransform: "uppercase",
        color: eyebrowCol,
        marginTop: 12,
      }}>{eyebrow}</div>

      <h3 style={{
        fontFamily: "var(--font-display)",
        fontWeight: 800,
        fontSize: visual === "large" ? "clamp(28px, 2.6vw, 40px)" : "clamp(22px, 2vw, 28px)",
        lineHeight: 1.05,
        letterSpacing: "-0.025em",
        color: fg,
        margin: 0,
        textWrap: "balance",
      }}>{title}</h3>

      <p style={{
        fontFamily: "var(--font-body)",
        fontSize: visual === "large" ? 15 : 14,
        lineHeight: 1.55,
        color: sub,
        margin: 0,
        maxWidth: 480,
        textWrap: "pretty",
      }}>{desc}</p>

      {/* Bottom: chips + arrow */}
      <div style={{
        marginTop: "auto",
        paddingTop: 20,
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "space-between",
        gap: 16,
      }}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
          {chips.map(c => (
            <span key={c} style={{
              fontFamily: "var(--font-body)",
              fontSize: 11,
              fontWeight: 600,
              padding: "5px 12px",
              borderRadius: 999,
              background: dark || accent ? "rgba(255,255,255,0.12)" : "rgba(14,16,20,0.06)",
              color: dark || accent ? "rgba(255,255,255,0.92)" : "var(--fg-2)",
              border: dark || accent ? "1px solid rgba(255,255,255,0.08)" : "1px solid transparent",
            }}>{c}</span>
          ))}
        </div>

        <a href="#contacto" aria-label="Cotizar" style={{
          flexShrink: 0,
          width: 44, height: 44,
          borderRadius: "50%",
          background: dark ? "var(--accent)" : accent ? "#fff" : "var(--ink)",
          color: dark ? "#fff" : accent ? "var(--accent)" : "var(--paper)",
          display: "inline-flex", alignItems: "center", justifyContent: "center",
          textDecoration: "none",
          transition: "transform var(--dur-fast) var(--ease-out)",
          transform: hover ? "rotate(-45deg)" : "rotate(0deg)",
        }}>
          <i data-lucide="arrow-right" width="18" height="18" {...{"stroke-width":"2.2"}}></i>
        </a>
      </div>

      {/* Big subtle glyph for "large" variant */}
      {visual === "large" && (
        <div style={{
          position: "absolute",
          right: -20, bottom: -40,
          fontFamily: "var(--font-display)",
          fontWeight: 900,
          fontSize: 260,
          lineHeight: 1,
          color: "rgba(14,16,20,0.04)",
          letterSpacing: "-0.05em",
          pointerEvents: "none",
        }}>01</div>
      )}
      {visual === "industrial" && (
        <div style={{
          position: "absolute",
          inset: "auto -40px -60px auto",
          width: 280, height: 280,
          background: "radial-gradient(circle, rgba(232,115,44,0.18), transparent 70%)",
          pointerEvents: "none",
        }} />
      )}
    </article>
  );
}

window.ServiceLines = ServiceLines;
