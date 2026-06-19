/*
    Repository analysis JavaScript.
 */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const languageData =
            window.languageData || {};

        const labels =
            Object.keys(languageData);

        const values =
            Object.values(languageData);

        if (!labels.length) {
            return;
        }

        const total =
            values.reduce(
                (sum, value) => sum + value,
                0
            );

        const percentages =
            values.map(
                value =>
                    (
                        (value / total) * 100
                    ).toFixed(1)
            );

        const githubColors = {
            "Python": "#3572A5",
            "JavaScript": "#f1e05a",
            "TypeScript": "#3178c6",
            "HTML": "#e34c26",
            "CSS": "#563d7c",
            "Java": "#b07219",
            "C": "#555555",
            "C++": "#f34b7d",
            "C#": "#178600",
            "Go": "#00ADD8",
            "Rust": "#dea584",
            "PHP": "#4F5D95",
            "Ruby": "#701516",
            "Swift": "#F05138",
            "Kotlin": "#A97BFF",
            "Shell": "#89e051"
        };

        const fallbackColors = [
            "#6366F1",
            "#06B6D4",
            "#10B981",
            "#F59E0B",
            "#EF4444",
            "#8B5CF6",
            "#EC4899"
        ];

        const colors =
            labels.map(
                (language, index) =>
                    githubColors[language]
                || fallbackColors[
                    index %
                        fallbackColors.length
                        ]
            );

        const ctx =
            document
                .getElementById(
                    "language-chart"
                )
                .getContext("2d");

        new Chart(
            ctx,
            {
                type: "pie",

                data: {
                    labels,

                    datasets: [
                        {
                            data: values,

                            backgroundColor:
                            colors,

                            borderWidth: 2,

                            borderColor:
                                "#ffffff"
                        }
                    ]
                },

                options: {
                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        legend: {
                            display: false
                        },

                        tooltip: {

                            callbacks: {

                                label:
                                function (
                                    context
                                ) {

                                    return (
                                        context.label +
                                         ": " +
                                         percentages[
                                             context.dataIndex
                                             ] +
                                            "%"
                                    );
                                }
                            }
                        }
                    }
                }
            }
        );

        const legend =
            document.getElementById(
                "language-legend"
            );

        labels.forEach(
            (
                language,
                    index
            ) => {
                const item =
                    document.createElement(
                        "div"
                    );

                item.classList.add(
                    "legend-item"
                );

                item.innerHTML = `
                <span
                    class="legend-color"
                    style="background:${colors[index]}"
                    ></span>
                    
                <span>
                    ${language}
                    (${percentages[index]}%)
                </span>
                `;

                legend.appendChild(
                    item
                );
            }
        );
    }
);
