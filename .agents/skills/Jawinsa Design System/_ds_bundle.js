/* @ds-bundle: {"format":3,"namespace":"JawinsaDesignSystem_ab7918","components":[],"sourceHashes":{"ui_kits/landing/Contact.jsx":"71c8a0b0936a","ui_kits/landing/Footer.jsx":"bc7259fdeb99","ui_kits/landing/Hero.jsx":"5b2ce139be9d","ui_kits/landing/Navbar.jsx":"a1686aefac00","ui_kits/landing/News.jsx":"44e0aaadcdf8","ui_kits/landing/ServiceLines.jsx":"ab01cb822b44","ui_kits/landing/WhyJawinsa.jsx":"894ffa85c2d7"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.JawinsaDesignSystem_ab7918 = window.JawinsaDesignSystem_ab7918 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// ui_kits/landing/Contact.jsx
try { (() => {
/* global React */
const {
  useState,
  useEffect,
  useRef
} = React;
function Contact() {
  const [sent, setSent] = useState(false);
  const [form, setForm] = useState({
    nombre: "",
    empresa: "",
    telefono: "",
    email: "",
    servicio: "Diagnóstico multimarca",
    mensaje: ""
  });
  const update = k => e => setForm({
    ...form,
    [k]: e.target.value
  });
  const submit = e => {
    e.preventDefault();
    setSent(true);
    setTimeout(() => setSent(false), 4000);
  };
  const ref = useRef(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    if (!ref.current) return;
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        setInView(true);
        io.disconnect();
      }
    }, {
      threshold: 0.1
    });
    io.observe(ref.current);
    return () => io.disconnect();
  }, []);
  return /*#__PURE__*/React.createElement("section", {
    id: "contacto",
    className: "section",
    ref: ref
  }, /*#__PURE__*/React.createElement("div", {
    className: "container"
  }, /*#__PURE__*/React.createElement("div", {
    className: `reveal ${inView ? "in" : ""}`,
    style: {
      display: "grid",
      gridTemplateColumns: "1.2fr 1fr",
      gap: 14,
      alignItems: "stretch"
    }
  }, /*#__PURE__*/React.createElement("form", {
    onSubmit: submit,
    style: {
      background: "var(--paper-elevated)",
      border: "1px solid rgba(14,16,20,0.05)",
      borderRadius: 32,
      padding: "clamp(32px, 4vw, 48px)",
      display: "flex",
      flexDirection: "column",
      gap: 20,
      boxShadow: "var(--shadow-soft)"
    },
    className: "contact-form"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow"
  }, /*#__PURE__*/React.createElement("span", {
    className: "dot"
  }), "Contacto"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: "clamp(28px, 3vw, 44px)",
      lineHeight: 1.05,
      letterSpacing: "-0.025em",
      margin: "16px 0 0",
      color: "var(--fg-1)",
      textWrap: "balance"
    }
  }, "Solicite su cotizaci\xF3n.", /*#__PURE__*/React.createElement("br", null), "Respondemos en menos de 24 h.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: 14
    },
    className: "ftwo"
  }, /*#__PURE__*/React.createElement("div", {
    className: "field"
  }, /*#__PURE__*/React.createElement("label", null, "Nombre completo"), /*#__PURE__*/React.createElement("input", {
    type: "text",
    required: true,
    value: form.nombre,
    onChange: update("nombre"),
    placeholder: "Andr\xE9s Tello"
  })), /*#__PURE__*/React.createElement("div", {
    className: "field"
  }, /*#__PURE__*/React.createElement("label", null, "Empresa (opcional)"), /*#__PURE__*/React.createElement("input", {
    type: "text",
    value: form.empresa,
    onChange: update("empresa"),
    placeholder: "Log\xEDstica del Sur S.A."
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: 14
    },
    className: "ftwo"
  }, /*#__PURE__*/React.createElement("div", {
    className: "field"
  }, /*#__PURE__*/React.createElement("label", null, "Tel\xE9fono / WhatsApp"), /*#__PURE__*/React.createElement("input", {
    type: "tel",
    required: true,
    value: form.telefono,
    onChange: update("telefono"),
    placeholder: "+51 999 123 456"
  })), /*#__PURE__*/React.createElement("div", {
    className: "field"
  }, /*#__PURE__*/React.createElement("label", null, "Correo"), /*#__PURE__*/React.createElement("input", {
    type: "email",
    required: true,
    value: form.email,
    onChange: update("email"),
    placeholder: "usted@empresa.com"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "field"
  }, /*#__PURE__*/React.createElement("label", null, "Servicio requerido"), /*#__PURE__*/React.createElement("select", {
    value: form.servicio,
    onChange: update("servicio")
  }, /*#__PURE__*/React.createElement("option", null, "Diagn\xF3stico multimarca"), /*#__PURE__*/React.createElement("option", null, "Mantenimiento preventivo \u2014 auto particular"), /*#__PURE__*/React.createElement("option", null, "Mantenimiento de flota (camiones / volquetes)"), /*#__PURE__*/React.createElement("option", null, "Servicio t\xE9cnico montacargas"), /*#__PURE__*/React.createElement("option", null, "Servicio t\xE9cnico grupos electr\xF3genos"), /*#__PURE__*/React.createElement("option", null, "Compra de repuestos / consumibles"), /*#__PURE__*/React.createElement("option", null, "Licitaci\xF3n / contrato corporativo"))), /*#__PURE__*/React.createElement("div", {
    className: "field"
  }, /*#__PURE__*/React.createElement("label", null, "Detalle del servicio"), /*#__PURE__*/React.createElement("textarea", {
    value: form.mensaje,
    onChange: update("mensaje"),
    placeholder: "Marca, modelo, a\xF1o, kilometraje y descripci\xF3n de la falla."
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      flexWrap: "wrap",
      gap: 12,
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 12,
      color: "var(--fg-3)",
      margin: 0,
      maxWidth: 320
    }
  }, "Sin spam \u2014 respuesta en menos de 24 h h\xE1biles."), /*#__PURE__*/React.createElement("button", {
    type: "submit",
    className: "btn btn-primary btn-lg",
    disabled: sent
  }, sent ? "Enviado ✓" : /*#__PURE__*/React.createElement(React.Fragment, null, "Solicitar cotizaci\xF3n", /*#__PURE__*/React.createElement("i", {
    "data-lucide": "arrow-up-right",
    width: "18",
    height: "18",
    "stroke-width": "2.2"
  }))))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(ContactCard, {
    icon: "message-circle",
    eyebrow: "WHATSAPP \xB7 M\xC1S R\xC1PIDO",
    title: "+51 999 123 456",
    desc: "Respuesta inmediata \xB7 Emergencias 24/7",
    href: "https://wa.me/51999123456",
    theme: "accent",
    big: true
  }), /*#__PURE__*/React.createElement(ContactCard, {
    icon: "phone",
    eyebrow: "LLAMAR",
    title: "(01) 234-5678",
    desc: "Lun \u2013 S\xE1b \xB7 7:00 \u2014 19:00",
    href: "tel:+5112345678"
  }), /*#__PURE__*/React.createElement(ContactCard, {
    icon: "map-pin",
    eyebrow: "VISITAR EL TALLER",
    title: "Av. Ejemplo 1234, Ate",
    desc: "Lima, Per\xFA \xB7 Estacionamiento para pesados",
    href: "#",
    theme: "dark"
  })))), /*#__PURE__*/React.createElement("style", null, `
        @media (max-width: 900px) {
          #contacto .reveal > div, #contacto .reveal {
            grid-template-columns: 1fr !important;
          }
          #contacto .ftwo { grid-template-columns: 1fr !important; }
        }
      `));
}
function ContactCard({
  icon,
  eyebrow,
  title,
  desc,
  href,
  theme,
  big
}) {
  const [hover, setHover] = useState(false);
  const accent = theme === "accent";
  const dark = theme === "dark";
  const bg = accent ? "var(--accent)" : dark ? "var(--ink)" : "var(--paper-elevated)";
  const fg = accent || dark ? "var(--paper)" : "var(--fg-1)";
  const sub = accent ? "rgba(255,255,255,0.9)" : dark ? "var(--steel-300)" : "var(--fg-2)";
  const ey = accent ? "rgba(255,255,255,0.78)" : dark ? "var(--steel-400)" : "var(--fg-3)";
  return /*#__PURE__*/React.createElement("a", {
    href: href,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      background: bg,
      color: fg,
      borderRadius: 28,
      padding: big ? "28px 32px" : "22px 26px",
      textDecoration: "none",
      display: "flex",
      gap: 18,
      alignItems: "flex-start",
      boxShadow: hover ? "var(--shadow-2)" : "var(--shadow-soft)",
      border: accent || dark ? "1px solid transparent" : "1px solid rgba(14,16,20,0.05)",
      transition: "box-shadow var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out)",
      transform: hover ? "translateY(-2px)" : "translateY(0)",
      position: "relative",
      overflow: "hidden",
      flex: big ? 1.4 : 1,
      minHeight: big ? 180 : "auto"
    }
  }, accent && /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: "auto -60px -60px auto",
      width: 220,
      height: 220,
      background: "radial-gradient(circle, rgba(255,255,255,0.18), transparent 70%)",
      pointerEvents: "none"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      width: big ? 56 : 44,
      height: big ? 56 : 44,
      flexShrink: 0,
      borderRadius: 16,
      background: accent || dark ? "rgba(255,255,255,0.18)" : "var(--ink)",
      color: accent || dark ? "#fff" : "var(--paper)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      zIndex: 1
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": icon,
    width: big ? 24 : 20,
    height: big ? 24 : 20,
    "stroke-width": "1.75"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 6,
      position: "relative",
      zIndex: 1,
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontWeight: 700,
      fontSize: 10,
      letterSpacing: "0.22em",
      color: ey
    }
  }, eyebrow), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: big ? 28 : 22,
      lineHeight: 1.05,
      letterSpacing: "-0.02em"
    }
  }, title), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 13,
      color: sub
    }
  }, desc)), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 36,
      height: 36,
      borderRadius: "50%",
      background: accent || dark ? "rgba(255,255,255,0.16)" : "rgba(14,16,20,0.06)",
      color: accent || dark ? "#fff" : "var(--fg-1)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      zIndex: 1,
      flexShrink: 0,
      transition: "transform var(--dur-fast) var(--ease-out)",
      transform: hover ? "rotate(-45deg)" : "rotate(0deg)"
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "arrow-right",
    width: "16",
    height: "16",
    "stroke-width": "2"
  })));
}
window.Contact = Contact;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/landing/Contact.jsx", error: String((e && e.message) || e) }); }

// ui_kits/landing/Footer.jsx
try { (() => {
/* global React */

function Footer() {
  return /*#__PURE__*/React.createElement("footer", {
    style: {
      paddingTop: 24,
      paddingBottom: 24
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "container"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: "var(--ink)",
      color: "var(--paper)",
      borderRadius: 32,
      padding: "clamp(36px, 4vw, 56px)",
      position: "relative",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      right: -120,
      top: -120,
      width: 500,
      height: 500,
      background: "radial-gradient(circle, rgba(232,115,44,0.16), transparent 65%)",
      pointerEvents: "none"
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "footer-grid",
    style: {
      position: "relative",
      zIndex: 1,
      display: "grid",
      gridTemplateColumns: "1.6fr 1fr 1fr 1fr",
      gap: 48,
      paddingBottom: 48,
      borderBottom: "1px solid rgba(246,244,240,0.08)"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logo-placeholder-dark.svg",
    alt: "Jawinsa",
    style: {
      height: 38,
      marginBottom: 24
    }
  }), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 14,
      lineHeight: 1.6,
      color: "var(--steel-300)",
      margin: 0,
      maxWidth: 320
    }
  }, "Taller multimarca e industrial. Reparaci\xF3n, mantenimiento y repuestos para veh\xEDculos, montacargas y grupos electr\xF3genos."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 10,
      marginTop: 28
    }
  }, /*#__PURE__*/React.createElement(SocialIcon, {
    icon: "message-circle"
  }), /*#__PURE__*/React.createElement(SocialIcon, {
    icon: "phone"
  }), /*#__PURE__*/React.createElement(SocialIcon, {
    icon: "mail"
  }), /*#__PURE__*/React.createElement(SocialIcon, {
    icon: "instagram"
  }))), /*#__PURE__*/React.createElement(FooterCol, {
    title: "Servicios",
    items: ["Línea automotriz", "Línea comercial", "Línea industrial", "Repuestos & consumibles", "Diagnóstico OBD-II"]
  }), /*#__PURE__*/React.createElement(FooterCol, {
    title: "Empresa",
    items: ["Nosotros", "Equipo técnico", "Casos de éxito", "Licitaciones", "Trabaja con nosotros"]
  }), /*#__PURE__*/React.createElement(FooterCol, {
    title: "Contacto",
    items: ["+51 999 123 456", "(01) 234-5678", "ventas@jawinsa.pe", "Av. Ejemplo 1234, Ate", "Lun–Sáb · 7:00 – 19:00"],
    mono: true
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      zIndex: 1,
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      paddingTop: 24,
      flexWrap: "wrap",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: 11,
      color: "var(--steel-500)",
      letterSpacing: "0.04em"
    }
  }, "\xA9 2026 Jawinsa S.A.C. \xB7 RUC 20XXXXXXXXX \xB7 Hecho en Lima"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 24
    }
  }, /*#__PURE__*/React.createElement("a", {
    href: "#",
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 12,
      color: "var(--steel-400)",
      textDecoration: "none"
    }
  }, "Pol\xEDtica de privacidad"), /*#__PURE__*/React.createElement("a", {
    href: "#",
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 12,
      color: "var(--steel-400)",
      textDecoration: "none"
    }
  }, "T\xE9rminos"))))), /*#__PURE__*/React.createElement("style", null, `
        @media (max-width: 900px) {
          .footer-grid { grid-template-columns: 1fr 1fr !important; }
        }
        @media (max-width: 560px) {
          .footer-grid { grid-template-columns: 1fr !important; }
        }
      `));
}
function FooterCol({
  title,
  items,
  mono
}) {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontWeight: 700,
      fontSize: 11,
      letterSpacing: "0.22em",
      textTransform: "uppercase",
      color: "var(--steel-400)",
      marginBottom: 18
    }
  }, title), /*#__PURE__*/React.createElement("ul", {
    style: {
      listStyle: "none",
      padding: 0,
      margin: 0,
      display: "flex",
      flexDirection: "column",
      gap: 12
    }
  }, items.map(it => /*#__PURE__*/React.createElement("li", {
    key: it
  }, /*#__PURE__*/React.createElement("a", {
    href: "#",
    style: {
      fontFamily: mono ? "var(--font-mono)" : "var(--font-body)",
      fontSize: mono ? 13 : 14,
      color: "var(--steel-300)",
      textDecoration: "none"
    },
    onMouseEnter: e => e.currentTarget.style.color = "var(--paper)",
    onMouseLeave: e => e.currentTarget.style.color = "var(--steel-300)"
  }, it)))));
}
function SocialIcon({
  icon
}) {
  return /*#__PURE__*/React.createElement("a", {
    href: "#",
    style: {
      width: 38,
      height: 38,
      borderRadius: 14,
      border: "1px solid rgba(246,244,240,0.12)",
      background: "rgba(246,244,240,0.04)",
      color: "var(--steel-300)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      textDecoration: "none",
      transition: "all 150ms var(--ease-out)"
    },
    onMouseEnter: e => {
      e.currentTarget.style.background = "var(--accent)";
      e.currentTarget.style.color = "#fff";
      e.currentTarget.style.borderColor = "var(--accent)";
    },
    onMouseLeave: e => {
      e.currentTarget.style.background = "rgba(246,244,240,0.04)";
      e.currentTarget.style.color = "var(--steel-300)";
      e.currentTarget.style.borderColor = "rgba(246,244,240,0.12)";
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": icon,
    width: "16",
    height: "16",
    "stroke-width": "1.75"
  }));
}
window.Footer = Footer;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/landing/Footer.jsx", error: String((e && e.message) || e) }); }

// ui_kits/landing/Hero.jsx
try { (() => {
/* global React */
const {
  useEffect,
  useRef,
  useState
} = React;
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
    window.addEventListener("scroll", onScroll, {
      passive: true
    });
    return () => {
      clearTimeout(t);
      window.removeEventListener("scroll", onScroll);
    };
  }, []);
  return /*#__PURE__*/React.createElement("header", {
    id: "top",
    style: {
      position: "relative",
      padding: "140px 0 60px",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      right: "-200px",
      top: "10%",
      width: 700,
      height: 700,
      background: "radial-gradient(circle, rgba(232,115,44,0.10), transparent 60%)",
      pointerEvents: "none",
      zIndex: 0
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "container",
    style: {
      position: "relative",
      zIndex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "hero-grid",
    style: {
      display: "grid",
      gridTemplateColumns: "1.05fr 1fr",
      gap: 40,
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: `reveal ${revealed ? "in" : ""}`,
    style: {
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
      marginBottom: 32
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 7,
      height: 7,
      borderRadius: 999,
      background: "var(--accent)"
    }
  }), "Taller multimarca \xB7 Lima, Per\xFA"), /*#__PURE__*/React.createElement("h1", {
    className: `reveal r-1 ${revealed ? "in" : ""}`,
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 900,
      fontSize: "clamp(48px, 6.5vw, 96px)",
      lineHeight: 0.96,
      letterSpacing: "-0.035em",
      margin: 0,
      color: "var(--fg-1)",
      textWrap: "balance"
    }
  }, "Reparamos", /*#__PURE__*/React.createElement("br", null), "lo que detiene", /*#__PURE__*/React.createElement("br", null), "su ", /*#__PURE__*/React.createElement("em", {
    style: {
      fontStyle: "normal",
      position: "relative",
      color: "var(--accent)"
    }
  }, "operaci\xF3n", /*#__PURE__*/React.createElement("svg", {
    style: {
      position: "absolute",
      left: 0,
      bottom: "-6px",
      width: "100%",
      height: 14,
      transition: "opacity 600ms 800ms",
      opacity: revealed ? 1 : 0
    },
    viewBox: "0 0 200 14",
    preserveAspectRatio: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M2 9 C 50 2, 110 13, 198 5",
    stroke: "currentColor",
    strokeWidth: "3",
    fill: "none",
    strokeLinecap: "round"
  }))), "."), /*#__PURE__*/React.createElement("p", {
    className: `reveal r-2 ${revealed ? "in" : ""}`,
    style: {
      fontFamily: "var(--font-body)",
      fontSize: "clamp(16px, 1.2vw, 19px)",
      lineHeight: 1.55,
      color: "var(--fg-2)",
      maxWidth: 540,
      margin: "48px 0 0"
    }
  }, "Taller industrial multimarca para autos, flotas, camiones, montacargas y grupos electr\xF3genos. Diagn\xF3stico electr\xF3nico avanzado y repuestos en una sola operaci\xF3n."), /*#__PURE__*/React.createElement("div", {
    className: `reveal r-3 ${revealed ? "in" : ""}`,
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: 12,
      marginTop: 36
    }
  }, /*#__PURE__*/React.createElement("a", {
    href: "#contacto",
    className: "btn btn-primary btn-lg"
  }, "Solicitar cotizaci\xF3n", /*#__PURE__*/React.createElement("i", {
    "data-lucide": "arrow-up-right",
    width: "18",
    height: "18",
    "stroke-width": "2.2"
  })), /*#__PURE__*/React.createElement("a", {
    href: "#servicios",
    className: "btn btn-ghost btn-lg"
  }, "Ver servicios"))), /*#__PURE__*/React.createElement("div", {
    ref: photoRef,
    className: `reveal r-2 ${revealed ? "in" : ""}`,
    style: {
      position: "relative",
      aspectRatio: "1/1",
      minHeight: 480,
      willChange: "transform"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "photo",
    style: {
      position: "absolute",
      inset: "8% 0 8% 8%",
      borderRadius: 28
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "photo-label"
  }, "HERO \xB7 VEHICLE / WORKSHOP"), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: "50%",
      top: "55%",
      transform: "translate(-50%, -50%)",
      fontFamily: "var(--font-display)",
      fontWeight: 900,
      fontSize: "clamp(80px, 14vw, 220px)",
      color: "rgba(14,16,20,0.06)",
      letterSpacing: "-0.05em",
      lineHeight: 1,
      pointerEvents: "none",
      userSelect: "none"
    }
  }, "J")), /*#__PURE__*/React.createElement("div", {
    className: `reveal r-3 ${revealed ? "in" : ""}`,
    style: {
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
      whiteSpace: "nowrap"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 40,
      height: 40,
      borderRadius: 14,
      background: "var(--ink)",
      color: "var(--paper)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "gauge",
    width: "20",
    height: "20",
    "stroke-width": "1.75"
  })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 11,
      fontWeight: 700,
      letterSpacing: "0.16em",
      textTransform: "uppercase",
      color: "var(--fg-3)"
    }
  }, "Diagn\xF3stico"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: 18,
      color: "var(--fg-1)",
      marginTop: 2
    }
  }, "OBD-II \xB7 45 min"))), /*#__PURE__*/React.createElement("div", {
    className: `reveal r-4 ${revealed ? "in" : ""}`,
    style: {
      position: "absolute",
      right: -14,
      top: "44%",
      padding: "20px 24px",
      borderRadius: 22,
      background: "var(--ink)",
      color: "var(--paper)",
      boxShadow: "var(--shadow-3)",
      minWidth: 220
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 11,
      fontWeight: 700,
      letterSpacing: "0.16em",
      textTransform: "uppercase",
      color: "var(--steel-400)"
    }
  }, "Atendidos / a\xF1o"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: 44,
      lineHeight: 1,
      color: "var(--paper)",
      marginTop: 6,
      fontVariantNumeric: "tabular-nums"
    }
  }, "800", /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--accent)"
    }
  }, "+")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8,
      fontFamily: "var(--font-body)",
      fontSize: 13,
      color: "var(--steel-300)"
    }
  }, "Unidades B2B \xB7 12 a\xF1os")), /*#__PURE__*/React.createElement("div", {
    className: `reveal r-5 ${revealed ? "in" : ""}`,
    style: {
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
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 8,
      height: 8,
      borderRadius: 999,
      background: "var(--success)",
      boxShadow: "0 0 0 3px rgba(46,132,99,0.18)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 13,
      fontWeight: 600,
      color: "var(--fg-1)"
    }
  }, "Atenci\xF3n 24/7 emergencias")))), /*#__PURE__*/React.createElement("div", {
    className: `reveal r-5 ${revealed ? "in" : ""} stat-strip`,
    style: {
      marginTop: 80,
      display: "grid",
      gridTemplateColumns: "repeat(4, 1fr)",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(StatCard, {
    n: "+12",
    suf: "a\xF1os",
    label: "manteniendo flotas"
  }), /*#__PURE__*/React.createElement(StatCard, {
    n: "800",
    suf: "+",
    label: "unidades atendidas / a\xF1o"
  }), /*#__PURE__*/React.createElement(StatCard, {
    n: "24/7",
    suf: "",
    label: "emergencias B2B",
    accent: true
  }), /*#__PURE__*/React.createElement(StatCard, {
    n: "100",
    suf: "%",
    label: "diagn\xF3stico multimarca"
  }))), /*#__PURE__*/React.createElement("style", null, `
        @media (max-width: 900px) {
          .hero-grid { grid-template-columns: 1fr !important; }
          .stat-strip { grid-template-columns: 1fr 1fr !important; }
        }
      `));
}
function StatCard({
  n,
  suf,
  label,
  accent
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: accent ? "var(--accent)" : "var(--paper-elevated)",
      color: accent ? "#fff" : "var(--fg-1)",
      border: "1px solid",
      borderColor: accent ? "var(--accent)" : "rgba(14,16,20,0.05)",
      borderRadius: 22,
      padding: "22px 24px",
      boxShadow: "var(--shadow-soft)",
      display: "flex",
      flexDirection: "column",
      gap: 4
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: "clamp(28px, 3vw, 40px)",
      lineHeight: 1,
      letterSpacing: "-0.02em",
      fontVariantNumeric: "tabular-nums"
    }
  }, n, suf && /*#__PURE__*/React.createElement("span", {
    style: {
      color: accent ? "rgba(255,255,255,0.7)" : "var(--accent)"
    }
  }, suf)), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 4,
      fontFamily: "var(--font-body)",
      fontSize: 12,
      color: accent ? "rgba(255,255,255,0.85)" : "var(--fg-2)",
      textWrap: "balance"
    }
  }, label));
}
window.Hero = Hero;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/landing/Hero.jsx", error: String((e && e.message) || e) }); }

// ui_kits/landing/Navbar.jsx
try { (() => {
/* global React */
const {
  useState,
  useEffect
} = React;
function Nav() {
  const [active, setActive] = useState("servicios");
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "topbar"
  }, /*#__PURE__*/React.createElement("a", {
    href: "#top",
    className: "logo-pill",
    "aria-label": "Jawinsa"
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logo-placeholder.svg",
    alt: "Jawinsa",
    style: {
      height: 22
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("a", {
    href: "tel:+5119991234",
    className: "btn btn-ghost",
    style: {
      display: "inline-flex",
      padding: "12px 18px",
      fontSize: 13
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "phone",
    width: "14",
    height: "14",
    "stroke-width": "2"
  }), "Llamar"), /*#__PURE__*/React.createElement("a", {
    href: "#contacto",
    className: "cta-pill"
  }, "Cotizar", /*#__PURE__*/React.createElement("i", {
    "data-lucide": "arrow-up-right",
    width: "14",
    height: "14",
    "stroke-width": "2.2"
  })))), /*#__PURE__*/React.createElement("nav", {
    className: "pillnav"
  }, [["servicios", "Servicios"], ["industrial", "Industrial"], ["nosotros", "Nosotros"], ["noticias", "Noticias"], ["contacto", "Contacto"]].map(([id, label]) => /*#__PURE__*/React.createElement("a", {
    key: id,
    href: `#${id}`,
    className: active === id ? "active" : "",
    onClick: () => setActive(id)
  }, label))), /*#__PURE__*/React.createElement("div", {
    className: "siderail"
  }, /*#__PURE__*/React.createElement("button", {
    className: "ic",
    title: "Diagn\xF3stico"
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "gauge",
    width: "20",
    height: "20",
    "stroke-width": "1.75"
  })), /*#__PURE__*/React.createElement("button", {
    className: "ic",
    title: "Repuestos"
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "cog",
    width: "20",
    height: "20",
    "stroke-width": "1.75"
  })), /*#__PURE__*/React.createElement("button", {
    className: "ic",
    title: "Mantenimiento"
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "wrench",
    width: "20",
    height: "20",
    "stroke-width": "1.75"
  })), /*#__PURE__*/React.createElement("button", {
    className: "ic accent",
    title: "WhatsApp"
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "message-circle",
    width: "20",
    height: "20",
    "stroke-width": "2"
  }))));
}
window.Nav = Nav;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/landing/Navbar.jsx", error: String((e && e.message) || e) }); }

// ui_kits/landing/News.jsx
try { (() => {
/* global React */
const {
  useEffect,
  useRef,
  useState
} = React;
const POSTS = [{
  id: 1,
  cat: "MANTENIMIENTO",
  date: "18 May 2026",
  read: "4 min",
  title: "Cómo extender la vida útil de un grupo electrógeno en planta",
  excerpt: "Cinco rutinas críticas que reducen averías y prolongan operación entre intervenciones mayores.",
  feature: true
}, {
  id: 2,
  cat: "FLOTAS B2B",
  date: "10 May 2026",
  read: "6 min",
  title: "Checklist multimarca para mantenimiento preventivo de camiones",
  excerpt: "Lo que separa una flota productiva de una flota detenida en el patio."
}, {
  id: 3,
  cat: "DIAGNÓSTICO",
  date: "28 Abr 2026",
  read: "3 min",
  title: "P0420 explicado: cuándo el catalizador realmente falla",
  excerpt: "Cuándo el código OBD-II indica catalizador, y cuándo es sólo un sensor."
}, {
  id: 4,
  cat: "INDUSTRIAL",
  date: "21 Abr 2026",
  read: "5 min",
  title: "Montacargas eléctricos vs combustión: cómo elegir",
  excerpt: "Costos por hora, ciclos de trabajo y requisitos de mantenimiento."
}];
function News() {
  return /*#__PURE__*/React.createElement("section", {
    id: "noticias",
    className: "section"
  }, /*#__PURE__*/React.createElement("div", {
    className: "container"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sec-head",
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: 32,
      alignItems: "end",
      marginBottom: 48
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow"
  }, /*#__PURE__*/React.createElement("span", {
    className: "dot"
  }), "Noticias & mantenimiento"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: "clamp(36px, 4.5vw, 64px)",
      lineHeight: 1.02,
      letterSpacing: "-0.03em",
      margin: "16px 0 0",
      textWrap: "balance",
      color: "var(--fg-1)"
    }
  }, "Gu\xEDas y novedades", /*#__PURE__*/React.createElement("br", null), "del taller.")), /*#__PURE__*/React.createElement("a", {
    href: "#",
    className: "btn btn-ghost",
    style: {
      justifySelf: "end"
    }
  }, "Ver todas las publicaciones", /*#__PURE__*/React.createElement("i", {
    "data-lucide": "arrow-up-right",
    width: "14",
    height: "14",
    "stroke-width": "2.2"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "news-grid",
    style: {
      display: "grid",
      gridTemplateColumns: "1.4fr 1fr",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(FeaturePost, {
    post: POSTS[0]
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 14
    }
  }, POSTS.slice(1).map(p => /*#__PURE__*/React.createElement(ListPost, {
    key: p.id,
    post: p
  })))), /*#__PURE__*/React.createElement("style", null, `
          @media (max-width: 900px) {
            .news-grid { grid-template-columns: 1fr !important; }
            #noticias .sec-head { grid-template-columns: 1fr !important; }
            #noticias .sec-head .btn { justify-self: start !important; }
          }
        `)));
}
function useInView() {
  const ref = useRef(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    if (!ref.current) return;
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        setInView(true);
        io.disconnect();
      }
    }, {
      threshold: 0.15
    });
    io.observe(ref.current);
    return () => io.disconnect();
  }, []);
  return [ref, inView];
}
function FeaturePost({
  post
}) {
  const [ref, inView] = useInView();
  const [hover, setHover] = useState(false);
  return /*#__PURE__*/React.createElement("article", {
    ref: ref,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    className: `reveal ${inView ? "in" : ""}`,
    style: {
      background: "var(--paper-elevated)",
      border: "1px solid rgba(14,16,20,0.05)",
      borderRadius: 28,
      overflow: "hidden",
      boxShadow: hover ? "var(--shadow-2)" : "var(--shadow-soft)",
      transition: "box-shadow var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out)",
      transform: hover ? "translateY(-2px)" : "translateY(0)",
      display: "flex",
      flexDirection: "column"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "photo",
    style: {
      aspectRatio: "16/10",
      borderRadius: 0,
      position: "relative"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "photo-label"
  }, "FEATURE \xB7 HERO PHOTO"), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      top: 18,
      left: 18,
      padding: "6px 14px",
      borderRadius: 999,
      background: "rgba(14,16,20,0.85)",
      backdropFilter: "blur(12px)",
      color: "var(--paper)",
      fontFamily: "var(--font-body)",
      fontWeight: 700,
      fontSize: 11,
      letterSpacing: "0.18em"
    }
  }, post.cat)), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "32px 32px 36px",
      display: "flex",
      flexDirection: "column",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 12,
      fontFamily: "var(--font-mono)",
      fontSize: 12,
      color: "var(--fg-3)"
    }
  }, /*#__PURE__*/React.createElement("span", null, post.date), /*#__PURE__*/React.createElement("span", null, "\xB7"), /*#__PURE__*/React.createElement("span", null, post.read, " de lectura")), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: "clamp(24px, 2.6vw, 36px)",
      lineHeight: 1.08,
      letterSpacing: "-0.025em",
      margin: 0,
      textWrap: "balance",
      color: "var(--fg-1)"
    }
  }, post.title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 15,
      lineHeight: 1.55,
      color: "var(--fg-2)",
      margin: 0,
      textWrap: "pretty"
    }
  }, post.excerpt), /*#__PURE__*/React.createElement("a", {
    href: "#",
    className: "btn btn-primary",
    style: {
      alignSelf: "flex-start",
      marginTop: 8
    }
  }, "Leer art\xEDculo", /*#__PURE__*/React.createElement("i", {
    "data-lucide": "arrow-up-right",
    width: "14",
    height: "14",
    "stroke-width": "2.2"
  }))));
}
function ListPost({
  post
}) {
  const [ref, inView] = useInView();
  const [hover, setHover] = useState(false);
  return /*#__PURE__*/React.createElement("a", {
    ref: ref,
    href: "#",
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    className: `reveal ${inView ? "in" : ""}`,
    style: {
      display: "grid",
      gridTemplateColumns: "100px 1fr auto",
      gap: 16,
      alignItems: "center",
      background: "var(--paper-elevated)",
      border: "1px solid rgba(14,16,20,0.05)",
      borderRadius: 22,
      padding: 16,
      textDecoration: "none",
      color: "inherit",
      boxShadow: hover ? "var(--shadow-2)" : "var(--shadow-soft)",
      transition: "box-shadow var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out)",
      transform: hover ? "translateX(2px)" : "translateX(0)",
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "photo",
    style: {
      aspectRatio: "1/1",
      borderRadius: 14
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 4,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontWeight: 700,
      fontSize: 10,
      letterSpacing: "0.22em",
      color: "var(--accent)"
    }
  }, post.cat), /*#__PURE__*/React.createElement("h4", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 700,
      fontSize: 18,
      lineHeight: 1.15,
      letterSpacing: "-0.015em",
      margin: 0,
      textWrap: "balance",
      color: "var(--fg-1)"
    }
  }, post.title), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 4,
      fontFamily: "var(--font-mono)",
      fontSize: 11,
      color: "var(--fg-3)"
    }
  }, post.date, " \xB7 ", post.read)), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 40,
      height: 40,
      borderRadius: "50%",
      background: hover ? "var(--ink)" : "rgba(14,16,20,0.06)",
      color: hover ? "var(--paper)" : "var(--fg-1)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      transition: "background var(--dur-fast) var(--ease-out), color var(--dur-fast) var(--ease-out)",
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "arrow-up-right",
    width: "18",
    height: "18",
    "stroke-width": "2"
  })));
}
window.News = News;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/landing/News.jsx", error: String((e && e.message) || e) }); }

// ui_kits/landing/ServiceLines.jsx
try { (() => {
/* global React */
const {
  useEffect,
  useState,
  useRef
} = React;
function ServiceLines() {
  return /*#__PURE__*/React.createElement("section", {
    id: "servicios",
    className: "section"
  }, /*#__PURE__*/React.createElement("div", {
    className: "container"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sec-head",
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: 32,
      alignItems: "end",
      marginBottom: 48
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow"
  }, /*#__PURE__*/React.createElement("span", {
    className: "dot"
  }), "L\xEDneas de servicio"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: "clamp(36px, 4.5vw, 64px)",
      lineHeight: 1.02,
      letterSpacing: "-0.03em",
      margin: "16px 0 0",
      textWrap: "balance",
      color: "var(--fg-1)"
    }
  }, "Cuatro l\xEDneas.", /*#__PURE__*/React.createElement("br", null), "Una operaci\xF3n integral.")), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 17,
      lineHeight: 1.55,
      color: "var(--fg-2)",
      margin: 0,
      maxWidth: 480,
      justifySelf: "end"
    }
  }, "Atendemos desde un sed\xE1n particular hasta una flota de volquetes o un grupo electr\xF3geno cr\xEDtico \u2014 multimarca, con diagn\xF3stico avanzado y repuestos en stock.")), /*#__PURE__*/React.createElement("div", {
    className: "bento",
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(12, 1fr)",
      gridAutoRows: "minmax(220px, auto)",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(BentoCard, {
    span: "span 7 / span 7",
    rowSpan: "span 2",
    eyebrow: "L\xCDNEA AUTOMOTRIZ",
    title: "Autos & camionetas",
    desc: "Mantenimiento preventivo y correctivo multimarca. Cambios de aceite, frenos, suspensi\xF3n, transmisi\xF3n y diagn\xF3stico electr\xF3nico OBD-II.",
    icon: "car",
    chips: ["Sedán", "SUV", "Pickup", "Híbrido"],
    visual: "large"
  }), /*#__PURE__*/React.createElement(BentoCard, {
    span: "span 5 / span 5",
    rowSpan: "span 2",
    eyebrow: "L\xCDNEA INDUSTRIAL",
    title: "Montacargas & gensets",
    desc: "Especialistas en montacargas el\xE9ctricos y a combusti\xF3n, y en grupos electr\xF3genos Cummins, Perkins, Caterpillar.",
    icon: "forklift",
    chips: ["Cummins", "Perkins", "Caterpillar"],
    theme: "dark",
    visual: "industrial"
  }), /*#__PURE__*/React.createElement(BentoCard, {
    span: "span 7 / span 7",
    eyebrow: "L\xCDNEA COMERCIAL",
    title: "Camiones & volquetes",
    desc: "Servicio t\xE9cnico para veh\xEDculos pesados de carga y construcci\xF3n. Contratos de mantenimiento para flotas operativas.",
    icon: "truck",
    chips: ["Camiones", "Volquetes", "Buses"]
  }), /*#__PURE__*/React.createElement(BentoCard, {
    span: "span 5 / span 5",
    eyebrow: "REPUESTOS",
    title: "Repuestos & fluidos",
    desc: "Venta directa de repuestos OEM y aftermarket, aceites y filtros.",
    icon: "cog",
    chips: ["OEM", "Aceites", "Filtros"],
    theme: "accent"
  }))), /*#__PURE__*/React.createElement("style", null, `
        @media (max-width: 900px) {
          .sec-head { grid-template-columns: 1fr !important; gap: 16px !important; }
          .sec-head p { justify-self: start !important; }
          .bento { grid-template-columns: 1fr !important; }
          .bento > * { grid-column: span 1 / span 1 !important; grid-row: auto !important; }
        }
      `));
}
function BentoCard({
  span,
  rowSpan,
  eyebrow,
  title,
  desc,
  icon,
  chips,
  theme,
  visual
}) {
  const ref = useRef(null);
  const [inView, setInView] = useState(false);
  const [hover, setHover] = useState(false);
  useEffect(() => {
    if (!ref.current) return;
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        setInView(true);
        io.disconnect();
      }
    }, {
      threshold: 0.1
    });
    io.observe(ref.current);
    return () => io.disconnect();
  }, []);
  const dark = theme === "dark";
  const accent = theme === "accent";
  const bg = dark ? "var(--ink)" : accent ? "var(--accent)" : "var(--paper-elevated)";
  const fg = dark || accent ? "var(--paper)" : "var(--fg-1)";
  const sub = dark ? "var(--steel-300)" : accent ? "rgba(255,255,255,0.85)" : "var(--fg-2)";
  const eyebrowCol = dark ? "var(--steel-400)" : accent ? "rgba(255,255,255,0.7)" : "var(--fg-3)";
  return /*#__PURE__*/React.createElement("article", {
    ref: ref,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    className: `reveal ${inView ? "in" : ""}`,
    style: {
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
      minHeight: 220
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 44,
      height: 44,
      borderRadius: 14,
      background: dark || accent ? "rgba(255,255,255,0.12)" : "var(--ink)",
      color: dark || accent ? "#fff" : "var(--paper)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": icon,
    width: "22",
    height: "22",
    "stroke-width": "1.75"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 11,
      fontWeight: 700,
      letterSpacing: "0.22em",
      textTransform: "uppercase",
      color: eyebrowCol,
      marginTop: 12
    }
  }, eyebrow), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: visual === "large" ? "clamp(28px, 2.6vw, 40px)" : "clamp(22px, 2vw, 28px)",
      lineHeight: 1.05,
      letterSpacing: "-0.025em",
      color: fg,
      margin: 0,
      textWrap: "balance"
    }
  }, title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: visual === "large" ? 15 : 14,
      lineHeight: 1.55,
      color: sub,
      margin: 0,
      maxWidth: 480,
      textWrap: "pretty"
    }
  }, desc), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "auto",
      paddingTop: 20,
      display: "flex",
      alignItems: "flex-end",
      justifyContent: "space-between",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: 6
    }
  }, chips.map(c => /*#__PURE__*/React.createElement("span", {
    key: c,
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 11,
      fontWeight: 600,
      padding: "5px 12px",
      borderRadius: 999,
      background: dark || accent ? "rgba(255,255,255,0.12)" : "rgba(14,16,20,0.06)",
      color: dark || accent ? "rgba(255,255,255,0.92)" : "var(--fg-2)",
      border: dark || accent ? "1px solid rgba(255,255,255,0.08)" : "1px solid transparent"
    }
  }, c))), /*#__PURE__*/React.createElement("a", {
    href: "#contacto",
    "aria-label": "Cotizar",
    style: {
      flexShrink: 0,
      width: 44,
      height: 44,
      borderRadius: "50%",
      background: dark ? "var(--accent)" : accent ? "#fff" : "var(--ink)",
      color: dark ? "#fff" : accent ? "var(--accent)" : "var(--paper)",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      textDecoration: "none",
      transition: "transform var(--dur-fast) var(--ease-out)",
      transform: hover ? "rotate(-45deg)" : "rotate(0deg)"
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": "arrow-right",
    width: "18",
    height: "18",
    "stroke-width": "2.2"
  }))), visual === "large" && /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      right: -20,
      bottom: -40,
      fontFamily: "var(--font-display)",
      fontWeight: 900,
      fontSize: 260,
      lineHeight: 1,
      color: "rgba(14,16,20,0.04)",
      letterSpacing: "-0.05em",
      pointerEvents: "none"
    }
  }, "01"), visual === "industrial" && /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: "auto -40px -60px auto",
      width: 280,
      height: 280,
      background: "radial-gradient(circle, rgba(232,115,44,0.18), transparent 70%)",
      pointerEvents: "none"
    }
  }));
}
window.ServiceLines = ServiceLines;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/landing/ServiceLines.jsx", error: String((e && e.message) || e) }); }

// ui_kits/landing/WhyJawinsa.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* global React */
const {
  useEffect,
  useRef,
  useState
} = React;
const PILLARS = [{
  icon: "shield-check",
  title: "Equipo certificado",
  desc: "Técnicos con certificación multimarca y herramientas de diagnóstico OBD-II actualizadas."
}, {
  icon: "gauge-circle",
  title: "Diagnóstico antes de cotizar",
  desc: "No reparamos a ciegas. Diagnóstico electrónico documentado y cotización detallada."
}, {
  icon: "badge-check",
  title: "Experiencia B2B comprobada",
  desc: "Contratos con flotas de logística, construcción y operadores. Postulamos a licitaciones."
}];
function WhyJawinsa() {
  const ref = useRef(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    if (!ref.current) return;
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        setInView(true);
        io.disconnect();
      }
    }, {
      threshold: 0.15
    });
    io.observe(ref.current);
    return () => io.disconnect();
  }, []);
  return /*#__PURE__*/React.createElement("section", {
    id: "nosotros",
    className: "section",
    ref: ref
  }, /*#__PURE__*/React.createElement("div", {
    className: "container"
  }, /*#__PURE__*/React.createElement("div", {
    className: `reveal ${inView ? "in" : ""}`
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: "var(--ink)",
      color: "var(--paper)",
      borderRadius: 32,
      padding: "clamp(40px, 5vw, 72px)",
      position: "relative",
      overflow: "hidden",
      boxShadow: "var(--shadow-3)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      right: -120,
      top: -120,
      width: 500,
      height: 500,
      background: "radial-gradient(circle, rgba(232,115,44,0.25), transparent 65%)",
      pointerEvents: "none"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: "-2%",
      bottom: "-30%",
      fontFamily: "var(--font-display)",
      fontWeight: 900,
      fontSize: 600,
      lineHeight: 1,
      color: "rgba(246,244,240,0.04)",
      letterSpacing: "-0.05em",
      pointerEvents: "none",
      userSelect: "none"
    }
  }, "J"), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      zIndex: 1,
      display: "grid",
      gridTemplateColumns: "1.1fr 1fr",
      gap: 48,
      alignItems: "end"
    },
    className: "why-head"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "eyebrow",
    style: {
      color: "var(--steel-400)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "dot"
  }), "Por qu\xE9 Jawinsa"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: "clamp(36px, 4.5vw, 64px)",
      lineHeight: 1.02,
      letterSpacing: "-0.03em",
      margin: "16px 0 0",
      color: "var(--paper)",
      textWrap: "balance"
    }
  }, "Confianza t\xE9cnica,", /*#__PURE__*/React.createElement("br", null), "no promesas de marketing.")), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 17,
      lineHeight: 1.55,
      color: "var(--steel-300)",
      margin: 0,
      maxWidth: 460,
      justifySelf: "end"
    }
  }, "Operamos con la disciplina de una flota industrial y la atenci\xF3n de un taller de barrio. Nuestros clientes vuelven porque devolvemos la unidad operativa, a tiempo y bien documentada.")), /*#__PURE__*/React.createElement("div", {
    className: "why-pillars",
    style: {
      marginTop: 64,
      position: "relative",
      zIndex: 1,
      display: "grid",
      gridTemplateColumns: "repeat(3, 1fr)",
      gap: 14
    }
  }, PILLARS.map((p, i) => /*#__PURE__*/React.createElement(Pillar, _extends({
    key: p.title
  }, p, {
    index: i
  })))), /*#__PURE__*/React.createElement("div", {
    className: "why-brands",
    style: {
      marginTop: 72,
      position: "relative",
      zIndex: 1,
      padding: "28px 0",
      borderTop: "1px solid rgba(246,244,240,0.08)",
      display: "grid",
      gridTemplateColumns: "auto 1fr",
      gap: 32,
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 11,
      fontWeight: 700,
      letterSpacing: "0.22em",
      textTransform: "uppercase",
      color: "var(--steel-400)",
      maxWidth: 180
    }
  }, "Marcas con las que trabajamos"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 40,
      flexWrap: "wrap",
      alignItems: "center",
      opacity: 0.85
    }
  }, ["TOYOTA", "HYUNDAI", "VOLVO", "CATERPILLAR", "CUMMINS", "PERKINS", "KOMATSU"].map(b => /*#__PURE__*/React.createElement("div", {
    key: b,
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 800,
      fontSize: 16,
      letterSpacing: "0.14em",
      color: "var(--steel-400)"
    }
  }, b))))))), /*#__PURE__*/React.createElement("style", null, `
        @media (max-width: 900px) {
          .why-head { grid-template-columns: 1fr !important; gap: 16px !important; }
          .why-head p { justify-self: start !important; }
          .why-pillars { grid-template-columns: 1fr !important; }
          .why-brands { grid-template-columns: 1fr !important; gap: 20px !important; }
        }
      `));
}
function Pillar({
  icon,
  title,
  desc,
  index
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: "rgba(246,244,240,0.04)",
      border: "1px solid rgba(246,244,240,0.08)",
      borderRadius: 22,
      padding: "28px 24px",
      display: "flex",
      flexDirection: "column",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 44,
      height: 44,
      borderRadius: 14,
      background: "var(--accent)",
      color: "#fff",
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    }
  }, /*#__PURE__*/React.createElement("i", {
    "data-lucide": icon,
    width: "22",
    height: "22",
    "stroke-width": "1.75"
  })), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontFamily: "var(--font-display)",
      fontWeight: 700,
      fontSize: 22,
      lineHeight: 1.15,
      letterSpacing: "-0.02em",
      color: "var(--paper)",
      margin: 0
    }
  }, title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontFamily: "var(--font-body)",
      fontSize: 14,
      lineHeight: 1.55,
      color: "var(--steel-300)",
      margin: 0
    }
  }, desc));
}
window.WhyJawinsa = WhyJawinsa;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/landing/WhyJawinsa.jsx", error: String((e && e.message) || e) }); }

})();
