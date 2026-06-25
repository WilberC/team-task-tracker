/* global React */
const { useEffect, useRef, useState } = React;

function Hero() {
  const [revealed, setRevealed] = useState(false);
  const photoRef = useRef(null);

  useEffect(() => {
    const t = setTimeout(() => setRevealed(true), 100);

    const onScroll = () => {
      if (!photoRef.current) return;
      const y = window.scrollY;
      photoRef.current.style.transform = `translate3d(0, ${y * 0.12}px, 0)`;
    };
    window.addEventListener("scroll", onScroll, { passive: true });

    return () => {
      clearTimeout(t);
      window.removeEventListener("scroll", onScroll);
    };
  }, []);

  return (
    <header id="top" style={{
      position: "relative",
      padding: "140px 0 60px",
      overflow: "hidden",
    }}>
      {/* Ambient blob */}
      <div style={{
        position: "absolute",
        right: "-200px",
        top: "10%",
        width: 700, height: 700,
        background: "radial-gradient(circle, rgba(232,115,44,0.10), transparent 60%)",
        pointerEvents: "none",
        zIndex: 0,
      }} />

      <div className="container" style={{ position: "relative", zIndex: 1 }}>
        <div className="hero-grid" style={{
          display: "grid",
          gridTemplateColumns: "1.05fr 1fr",
          gap: 40,
          alignItems: "center",
        }}>
          {/* LEFT — headline */}
          <div>
            <div className={`reveal ${revealed ? "in" : ""}`} style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 10,
              padding: "8px 16px",
              background: "var(--paper-elevated)",
              borderRadius: 999,
              border: "1px solid rgba(14,16,20,0.06)",
              boxShadow: "var(--shadow-soft)",
              fontFamily: "var(--font-body)",
              fontSize: 12,
              fontWeight: 600,
              letterSpacing: "0.16em",
              textTransform: "uppercase",
              color: "var(--fg-2)",
              marginBottom: 32,
            }}>
              <span style={{ width: 7, height: 7, borderRadius: 999, background: "var(--accent)" }} />
              Taller multimarca · Lima, Perú
            </div>

            <h1 className={`reveal r-1 ${revealed ? "in" : ""}`} style={{
              fontFamily: "var(--font-display)",
              fontWeight: 900,
              fontSize: "clamp(48px, 6.5vw, 96px)",
              lineHeight: 0.96,
              letterSpacing: "-0.035em",
              margin: 0,
              color: "var(--fg-1)",
              textWrap: "balance",
            }}>
              Reparamos<br />
              lo que detiene<br />
              su <em style={{
                fontStyle: "normal",
                position: "relative",
                color: "var(--accent)",
              }}>
                operación
                <svg style={{
                  position: "absolute",
                  left: 0, bottom: "-6px",
                  width: "100%", height: 14,
                  transition: "opacity 600ms 800ms",
                  opacity: revealed ? 1 : 0,
                }} viewBox="0 0 200 14" preserveAspectRatio="none">
                  <path d="M2 9 C 50 2, 110 13, 198 5" stroke="currentColor" strokeWidth="3" fill="none" strokeLinecap="round" />
                </svg>
              </em>.
            </h1>

            <p className={`reveal r-2 ${revealed ? "in" : ""}`} style={{
              fontFamily: "var(--font-body)",
              fontSize: "clamp(16px, 1.2vw, 19px)",
              lineHeight: 1.55,
              color: "var(--fg-2)",
              maxWidth: 540,
              margin: "48px 0 0",
            }}>
              Taller industrial multimarca para autos, flotas, camiones, montacargas
              y grupos electrógenos. Diagnóstico electrónico avanzado y repuestos
              en una sola operación.
            </p>

            <div className={`reveal r-3 ${revealed ? "in" : ""}`} style={{
              display: "flex", flexWrap: "wrap", gap: 12, marginTop: 36,
            }}>
              <a href="#contacto" className="btn btn-primary btn-lg">
                Solicitar cotización
                <i data-lucide="arrow-up-right" width="18" height="18" {...{"stroke-width":"2.2"}}></i>
              </a>
              <a href="#servicios" className="btn btn-ghost btn-lg">
                Ver servicios
              </a>
            </div>
          </div>

          {/* RIGHT — floating visual stack */}
          <div ref={photoRef} className={`reveal r-2 ${revealed ? "in" : ""}`} style={{
            position: "relative",
            aspectRatio: "1/1",
            minHeight: 480,
            willChange: "transform",
          }}>
            {/* Large vehicle photo */}
            <div className="photo" style={{
              position: "absolute",
              inset: "8% 0 8% 8%",
              borderRadius: 28,
            }}>
              <span className="photo-label">HERO · VEHICLE / WORKSHOP</span>
              {/* fake "vehicle" silhouette using divs */}
              <div style={{
                position: "absolute", left: "50%", top: "55%",
                transform: "translate(-50%, -50%)",
                fontFamily: "var(--font-display)",
                fontWeight: 900,
                fontSize: "clamp(80px, 14vw, 220px)",
                color: "rgba(14,16,20,0.06)",
                letterSpacing: "-0.05em",
                lineHeight: 1,
                pointerEvents: "none",
                userSelect: "none",
              }}>J</div>
            </div>

            {/* Float card 1 — Diagnóstico (top right) */}
            <div className={`reveal r-3 ${revealed ? "in" : ""}`} style={{
              position: "absolute",
              right: 0,
              top: 12,
              padding: "16px 20px",
              borderRadius: 22,
              background: "rgba(250, 248, 244, 0.85)",
              backdropFilter: "blur(20px) saturate(140%)",
              WebkitBackdropFilter: "blur(20px) saturate(140%)",
              border: "1px solid rgba(14,16,20,0.06)",
              boxShadow: "var(--shadow-2)",
              display: "flex",
              alignItems: "center",
              gap: 14,
              whiteSpace: "nowrap",
            }}>
              <div style={{
                width: 40, height: 40,
                borderRadius: 14,
                background: "var(--ink)",
                color: "var(--paper)",
                display: "flex", alignItems: "center", justifyContent: "center",
              }}>
                <i data-lucide="gauge" width="20" height="20" {...{"stroke-width":"1.75"}}></i>
              </div>
              <div>
                <div style={{
                  fontFamily: "var(--font-body)",
                  fontSize: 11,
                  fontWeight: 700,
                  letterSpacing: "0.16em",
                  textTransform: "uppercase",
                  color: "var(--fg-3)",
                }}>Diagnóstico</div>
                <div style={{
                  fontFamily: "var(--font-display)",
                  fontWeight: 800,
                  fontSize: 18,
                  color: "var(--fg-1)",
                  marginTop: 2,
                }}>OBD-II · 45 min</div>
              </div>
            </div>

            {/* Float card 2 — Stats / Power (mid right, accent) */}
            <div className={`reveal r-4 ${revealed ? "in" : ""}`} style={{
              position: "absolute",
              right: -14,
              top: "44%",
              padding: "20px 24px",
              borderRadius: 22,
              background: "var(--ink)",
              color: "var(--paper)",
              boxShadow: "var(--shadow-3)",
              minWidth: 220,
            }}>
              <div style={{
                fontFamily: "var(--font-body)",
                fontSize: 11,
                fontWeight: 700,
                letterSpacing: "0.16em",
                textTransform: "uppercase",
                color: "var(--steel-400)",
              }}>Atendidos / año</div>
              <div style={{
                fontFamily: "var(--font-display)",
                fontWeight: 800,
                fontSize: 44,
                lineHeight: 1,
                color: "var(--paper)",
                marginTop: 6,
                fontVariantNumeric: "tabular-nums",
              }}>
                800<span style={{ color: "var(--accent)" }}>+</span>
              </div>
              <div style={{
                marginTop: 8,
                fontFamily: "var(--font-body)",
                fontSize: 13,
                color: "var(--steel-300)",
              }}>Unidades B2B · 12 años</div>
            </div>

            {/* Float card 3 — Service tags (bottom left) */}
            <div className={`reveal r-5 ${revealed ? "in" : ""}`} style={{
              position: "absolute",
              left: -16,
              bottom: 28,
              padding: "12px 16px",
              borderRadius: 999,
              background: "rgba(250, 248, 244, 0.85)",
              backdropFilter: "blur(20px) saturate(140%)",
              WebkitBackdropFilter: "blur(20px) saturate(140%)",
              border: "1px solid rgba(14,16,20,0.06)",
              boxShadow: "var(--shadow-2)",
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}>
              <span style={{
                width: 8, height: 8, borderRadius: 999, background: "var(--success)",
                boxShadow: "0 0 0 3px rgba(46,132,99,0.18)",
              }} />
              <span style={{
                fontFamily: "var(--font-body)",
                fontSize: 13,
                fontWeight: 600,
                color: "var(--fg-1)",
              }}>Atención 24/7 emergencias</span>
            </div>
          </div>
        </div>

        {/* Bottom stat strip — bento style */}
        <div className={`reveal r-5 ${revealed ? "in" : ""} stat-strip`} style={{
          marginTop: 80,
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: 14,
        }}>
          <StatCard n="+12" suf="años" label="manteniendo flotas" />
          <StatCard n="800" suf="+" label="unidades atendidas / año" />
          <StatCard n="24/7" suf="" label="emergencias B2B" accent />
          <StatCard n="100" suf="%" label="diagnóstico multimarca" />
        </div>
      </div>

      <style>{`
        @media (max-width: 900px) {
          .hero-grid { grid-template-columns: 1fr !important; }
          .stat-strip { grid-template-columns: 1fr 1fr !important; }
        }
      `}</style>
    </header>
  );
}

function StatCard({ n, suf, label, accent }) {
  return (
    <div style={{
      background: accent ? "var(--accent)" : "var(--paper-elevated)",
      color: accent ? "#fff" : "var(--fg-1)",
      border: "1px solid",
      borderColor: accent ? "var(--accent)" : "rgba(14,16,20,0.05)",
      borderRadius: 22,
      padding: "22px 24px",
      boxShadow: "var(--shadow-soft)",
      display: "flex",
      flexDirection: "column",
      gap: 4,
    }}>
      <div style={{
        fontFamily: "var(--font-display)",
        fontWeight: 800,
        fontSize: "clamp(28px, 3vw, 40px)",
        lineHeight: 1,
        letterSpacing: "-0.02em",
        fontVariantNumeric: "tabular-nums",
      }}>
        {n}{suf && <span style={{ color: accent ? "rgba(255,255,255,0.7)" : "var(--accent)" }}>{suf}</span>}
      </div>
      <div style={{
        marginTop: 4,
        fontFamily: "var(--font-body)",
        fontSize: 12,
        color: accent ? "rgba(255,255,255,0.85)" : "var(--fg-2)",
        textWrap: "balance",
      }}>{label}</div>
    </div>
  );
}

window.Hero = Hero;
