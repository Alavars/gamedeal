import React, { useState, useEffect } from 'react';
import { X, ShieldCheck, FileText, Mail, Loader2, HelpCircle, Send, CheckCircle2, Clock } from 'lucide-react';
import { api } from '../api';

export default function InfoModal({ type, onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Quick message form state
  const [senderName, setSenderName] = useState('');
  const [senderEmail, setSenderEmail] = useState('');
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [sentSuccess, setSentSuccess] = useState(false);

  useEffect(() => {
    if (!type) return;
    setLoading(true);
    setSentSuccess(false);

    let fetcher;
    if (type === 'privacy') fetcher = api.getPrivacy;
    else if (type === 'terms') fetcher = api.getTerms;
    else fetcher = api.getContact;

    fetcher()
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [type]);

  if (!type) return null;

  const handleSendMessage = (e) => {
    e.preventDefault();
    setSending(true);
    setTimeout(() => {
      setSending(false);
      setSentSuccess(true);
      setMessage('');
      setTimeout(() => setSentSuccess(false), 5000);
    }, 800);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="bg-zinc-900 rounded-2xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-zinc-800 text-zinc-100 max-h-[88vh] overflow-y-auto relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-full bg-zinc-800 hover:bg-zinc-700 text-zinc-400 hover:text-white transition-colors cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {loading ? (
          <div className="p-16 flex flex-col items-center justify-center space-y-3">
            <Loader2 className="w-8 h-8 animate-spin text-zinc-300" />
            <p className="text-sm text-zinc-400">Loading information...</p>
          </div>
        ) : (
          <div>
            {/* Header */}
            <div className="flex items-center gap-3.5 mb-6 border-b border-zinc-800 pb-4">
              <div className="p-2.5 bg-zinc-800 text-white rounded-xl border border-zinc-700">
                {type === 'privacy' && <ShieldCheck className="w-6 h-6" />}
                {type === 'terms' && <FileText className="w-6 h-6" />}
                {type === 'contact' && <Mail className="w-6 h-6" />}
              </div>
              <div>
                <h2 className="text-2xl font-black text-white tracking-tight">
                  {data?.title}
                </h2>
                {data?.updated && (
                  <p className="text-xs text-zinc-400 mt-0.5">
                    Last updated: {data.updated}
                  </p>
                )}
              </div>
            </div>

            {/* Sections Content (Privacy & Terms) */}
            {data?.sections && (
              <div className="space-y-4 text-zinc-300">
                {data.sections.map((sec, idx) => (
                  <div key={idx} className="bg-zinc-950/70 p-4 rounded-xl border border-zinc-800/90">
                    <h3 className="font-bold text-sm text-white mb-1.5 flex items-center gap-1.5">
                      <span>{sec.heading}</span>
                    </h3>
                    <p className="text-xs leading-relaxed text-zinc-400">
                      {sec.content}
                    </p>
                  </div>
                ))}
              </div>
            )}

            {/* Contact Details, Support Form & FAQs */}
            {type === 'contact' && (
              <div className="space-y-6">
                {/* Contact badge */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-zinc-950/80 border border-zinc-800 p-4 rounded-xl">
                    <p className="text-xs font-semibold text-zinc-400">Official Support Email</p>
                    <a
                      href={`mailto:${data?.email}`}
                      className="text-lg font-bold text-white hover:underline block mt-1"
                    >
                      {data?.email}
                    </a>
                    <p className="text-xs text-zinc-400 mt-1 flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      <span>{data?.response_time}</span>
                    </p>
                  </div>

                  <div className="bg-zinc-950/80 border border-zinc-800 p-4 rounded-xl">
                    <p className="text-xs font-semibold text-zinc-400">Working Hours</p>
                    <p className="text-sm font-bold text-white mt-1">
                      {data?.office_hours || 'Mon–Fri: 09:00 – 18:00 UTC'}
                    </p>
                    <p className="text-xs text-zinc-500 mt-1">
                      Automated price checks operate 24/7.
                    </p>
                  </div>
                </div>

                {/* Direct Message Form */}
                <div className="bg-zinc-950/80 border border-zinc-800 p-5 rounded-2xl shadow-xs">
                  <h3 className="font-bold text-base text-white mb-3 flex items-center gap-2">
                    <Send className="w-4 h-4 text-zinc-300" />
                    <span>Send Us a Quick Message</span>
                  </h3>

                  {sentSuccess ? (
                    <div className="p-4 bg-zinc-900 border border-zinc-700 text-zinc-200 rounded-xl text-sm font-medium flex items-center gap-2">
                      <CheckCircle2 className="w-5 h-5 text-white flex-none" />
                      <span>Thank you! Your message has been sent to our support team.</span>
                    </div>
                  ) : (
                    <form onSubmit={handleSendMessage} className="space-y-3">
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <input
                          type="text"
                          required
                          placeholder="Your Name"
                          value={senderName}
                          onChange={(e) => setSenderName(e.target.value)}
                          className="w-full px-3 py-2 text-xs bg-zinc-900 border border-zinc-800 rounded-lg text-white focus:outline-hidden focus:ring-1 focus:ring-zinc-400"
                        />
                        <input
                          type="email"
                          required
                          placeholder="Your Email"
                          value={senderEmail}
                          onChange={(e) => setSenderEmail(e.target.value)}
                          className="w-full px-3 py-2 text-xs bg-zinc-900 border border-zinc-800 rounded-lg text-white focus:outline-hidden focus:ring-1 focus:ring-zinc-400"
                        />
                      </div>
                      <textarea
                        required
                        rows="3"
                        placeholder="How can we help you? (Bug report, feature request, question...)"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        className="w-full px-3 py-2 text-xs bg-zinc-900 border border-zinc-800 rounded-lg text-white focus:outline-hidden focus:ring-1 focus:ring-zinc-400 resize-none"
                      />
                      <button
                        type="submit"
                        disabled={sending}
                        className="bg-white hover:bg-zinc-200 text-black font-bold text-xs px-4 py-2 rounded-lg transition-colors flex items-center gap-1.5 cursor-pointer shadow-sm disabled:opacity-50"
                      >
                        {sending ? (
                          <Loader2 className="w-3.5 h-3.5 animate-spin text-black" />
                        ) : (
                          <Send className="w-3.5 h-3.5" />
                        )}
                        <span>{sending ? 'Sending...' : 'Send Message'}</span>
                      </button>
                    </form>
                  )}
                </div>

                {/* FAQs */}
                {data?.faqs && (
                  <div className="mt-4 space-y-3">
                    <h3 className="font-bold text-base text-white flex items-center gap-1.5">
                      <HelpCircle className="w-5 h-5 text-zinc-400" />
                      <span>Frequently Asked Questions</span>
                    </h3>
                    <div className="space-y-2.5">
                      {data.faqs.map((faq, idx) => (
                        <div key={idx} className="bg-zinc-950 p-3.5 rounded-xl border border-zinc-800/90">
                          <p className="font-bold text-xs text-white mb-1">
                            {faq.question}
                          </p>
                          <p className="text-xs text-zinc-400 leading-relaxed">
                            {faq.answer}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
