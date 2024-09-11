// pygoreadability.go
package pygoreadability

import (
    "fmt"
	"strings"
	"time"
    nurl "net/url"

    readability "github.com/go-shiori/go-readability"
	"github.com/go-shiori/dom"
)

func Parse(input string) (readability.Article, error) {
	parser := readability.NewParser()
	reader := strings.NewReader(input)
	doc, err := dom.FastParse(reader)
	if err != nil {
		return readability.Article{}, fmt.Errorf("failed to parse input: %v", err)
	}
	pageURL, _ := nurl.ParseRequestURI("http://fakehost.com")

	return parser.ParseDocument(doc, pageURL)
}

func FromURL(pageURL string, timeout time.Duration) (readability.Article, error) {
	return readability.FromURL(pageURL, timeout)
}

func GetTitle(article readability.Article) string {
	return article.Title
}

func GetContent(article readability.Article) string {
	return article.Content
}

func GetTextContent(article readability.Article) string {
	return article.TextContent
}