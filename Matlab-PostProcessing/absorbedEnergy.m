function dKE = absorbedEnergy(struct)

dKE = NaN;

IE = struct.DataAssembly{:,8};

dKE = IE(end);
end