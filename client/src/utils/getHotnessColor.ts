export const getHotnessColor = (hotness: string) => {
  const level = hotness.toLowerCase();
  if (level.includes("критическая")) {
    return "bg-red-600/20 text-red-800 border-red-300 font-bold";
  } else if (level.includes("высокая")) {
    return "bg-red-500/20 text-red-700 border-red-200";
  } else if (level.includes("средняя")) {
    return "bg-orange-500/20 text-orange-700 border-orange-200";
  } else if (level.includes("умеренная")) {
    return "bg-yellow-500/20 text-yellow-700 border-yellow-200";
  } else if (level.includes("низкая") || level.includes("спокойная")) {
    return "bg-green-500/20 text-green-700 border-green-200";
  }
  return "bg-gray-500/20 text-gray-700 border-gray-200";
};
