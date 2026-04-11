import React, { useEffect, useState } from 'react';

/**
 * Arkhe Horizon 3: Prosperity Tree Component
 * Refined Aesthetics: Glassmorphism, Neon Accents, and Topological Pulses.
 */
export const ProsperityTree: React.FC = () => {
    const [totalEarned, setTotalEarned] = useState("14,502.50");
    const [lastSync, setLastSync] = useState(new Date().toLocaleTimeString());

    return (
        <div className="p-8 bg-slate-950 rounded-[2rem] border border-cyan-500/20 shadow-[0_0_50px_rgba(6,182,212,0.1)] font-mono text-cyan-400">
            {/* Header: Global State */}
            <div className="flex justify-between items-start mb-12">
                <div>
                    <h2 className="text-4xl font-black text-white tracking-tighter uppercase italic">
                        🌳 Prosperity <span className="text-yellow-400">Tree</span>
                    </h2>
                    <p className="text-[10px] uppercase tracking-[0.3em] text-cyan-500/50 mt-2">
                        Arkhe-Block Mainnet Genesis | Bridge: <span className="text-green-400">Stable</span>
                    </p>
                </div>
                <div className="text-right bg-cyan-500/5 p-4 rounded-2xl border border-cyan-500/10">
                    <div className="text-3xl font-bold text-white">{totalEarned} <span className="text-sm">ASI</span></div>
                    <div className="text-[9px] uppercase tracking-widest text-cyan-500">Cumulative Revenue</div>
                </div>
            </div>

            {/* Central Visualization: Topological Map */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 h-[600px]">
                <div className="lg:col-span-3 bg-black/60 rounded-3xl border border-white/5 relative overflow-hidden flex items-center justify-center group">
                    {/* Animated Background Gradients */}
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(6,182,212,0.1),transparent_70%)]"></div>

                    {/* Simulated Topological Graph Nodes */}
                    <div className="relative z-10 text-center">
                        <div className="w-24 h-24 bg-yellow-400 rounded-full mx-auto mb-6 shadow-[0_0_60px_rgba(250,204,21,0.4)] flex items-center justify-center text-black text-4xl border-4 border-black group-hover:scale-110 transition-transform cursor-pointer">🧑</div>
                        <div className="text-xl font-bold text-white tracking-tight">Tecelão (Root)</div>
                        <div className="text-cyan-500/60 text-xs mt-1">Linhagem: 0x850...f432</div>

                        {/* Branches */}
                        <div className="mt-12 flex gap-16 justify-center">
                            {[
                                { name: "Video-A1", type: "agent", val: "2,401 ASI" },
                                { name: "Trans-A5", type: "agent", val: "1,850 ASI" }
                            ].map((branch, i) => (
                                <div key={i} className="flex flex-col items-center animate-bounce-slow" style={{ animationDelay: `${i*0.5}s` }}>
                                    <div className="w-1 h-8 bg-gradient-to-b from-cyan-500/40 to-transparent mb-4"></div>
                                    <div className="w-14 h-14 bg-cyan-900/40 rounded-2xl border border-cyan-500/30 flex items-center justify-center text-2xl shadow-lg">🤖</div>
                                    <span className="text-[10px] mt-2 font-bold text-white">{branch.name}</span>
                                    <span className="text-[9px] text-green-400">{branch.val}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="absolute top-6 right-6 flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-ping"></div>
                        <span className="text-[9px] uppercase tracking-tighter text-cyan-500/40">Real-time sync: {lastSync}</span>
                    </div>
                </div>

                {/* Sidebar: Analytics & Payouts */}
                <div className="space-y-6">
                    <div className="bg-white/5 p-6 rounded-3xl border border-white/5 backdrop-blur-md">
                        <h4 className="text-[10px] uppercase tracking-widest text-cyan-500 mb-4 font-black">Lineage Stats</h4>
                        <div className="space-y-4">
                            <div>
                                <div className="text-[10px] text-cyan-500/50 mb-1">Reputation Score</div>
                                <div className="text-2xl font-bold text-white">985 <span className="text-xs text-cyan-500">/ 1000</span></div>
                            </div>
                            <div>
                                <div className="text-[10px] text-cyan-500/50 mb-1">Active Derivatives</div>
                                <div className="text-2xl font-bold text-white">124 <span className="text-xs text-cyan-500">Nodes</span></div>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white/5 p-6 rounded-3xl border border-white/5 h-[280px] flex flex-col">
                        <h4 className="text-[10px] uppercase tracking-widest text-cyan-500 mb-4 font-black">Live Value Flow</h4>
                        <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar pr-2">
                            {[
                                { from: "Social-A2", amt: "4.1", color: "green" },
                                { from: "Edge-Prebid", amt: "0.8", color: "cyan" },
                                { from: "Auth-Sub", amt: "25.0", color: "green" },
                                { from: "Video-A1", amt: "12.4", color: "green" }
                            ].map((tx, i) => (
                                <div key={i} className="flex justify-between items-center text-[10px] border-b border-white/5 pb-2">
                                    <span className="text-white/70">{tx.from}</span>
                                    <span className={`text-${tx.color}-400 font-bold`}>+{tx.amt} ASI</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    <button className="group w-full py-5 bg-gradient-to-r from-yellow-400 to-amber-500 hover:from-yellow-300 hover:to-amber-400 text-black font-black uppercase tracking-widest rounded-[1.5rem] transition-all shadow-[0_10px_40px_rgba(250,204,21,0.2)] active:scale-95 overflow-hidden relative">
                        <span className="relative z-10">Claim Wealth</span>
                        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                    </button>
                </div>
            </div>

            <style dangerouslySetInnerHTML={{__html: `
                .animate-bounce-slow { animation: bounce 3s infinite; }
                @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
                .custom-scrollbar::-webkit-scrollbar { width: 3px; }
                .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(6,182,212,0.2); border-radius: 10px; }
            `}} />
        </div>
    );
};
